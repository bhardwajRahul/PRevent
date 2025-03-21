import json
from fastapi.logger import logger
from github import Repository, PullRequest, PullRequestComment, GithubException
from src.scan.detectors.utils import DetectionType
from src.settings import SCAN_CONTEXT, APP_REPO


def get_changed_files(
    repo: Repository,
    pr: PullRequest
) -> list[dict[str, str]]:

    # Requires Repository Permissions: Pull requests -> Read
    changes = pr.get_files()
    changed_files = []
    for file_changes in changes:
        if getattr(file_changes, 'patch', None) and '+0,0' not in file_changes.patch:
            try:
                changed_files.append({
                    "filename": file_changes.filename,
                    "diff": file_changes.patch
                })

            except KeyError as e:
                logger.error(
                    f"Missing key in {repo.name}/{file_changes.filename}, {file_changes}: {e}"
                )
            except UnicodeDecodeError as e:
                logger.error(
                    f"Error decoding file content for {repo.name}/{file_changes.filename}: {e}"
                )

    return changed_files


def get_file_full_content(repo, filename, pr) -> str:
    # Get full files because diff isn't enough to generate AST
    # Requires Repository Permissions: Contents -> Read
    try:
        return repo.get_contents(
            filename,
            ref=pr.head.sha
        ).decoded_content.decode('utf-8')

    except GithubException as e:
        logger.error(
            f"GitHub API error: {e}"
        )
    return ''


def determine_and_comment_scan_status(
    detections: list[DetectionType],
    pr: PullRequest,
    repo: Repository
) -> tuple:
    description = "Apiiro malicious-code scan"
    if detections:
        status = "failure"
        comment: PullRequestComment = comment_detections(detections, repo, pr)
        logger.info(
            f"PR #{pr.number} scan found: {json.dumps(detections)}"
        )
        return status, description, comment
    else:
        status = "success"
        comment = "Scan completed successfully."
        return status, description, comment


def comment_detections(
    detections: list[DetectionType],
    repo: Repository,
    pr: PullRequest
) -> PullRequestComment:
    landmark_string = f"{repo.full_name}, PR #{pr.number}"
    comment = None
    try:
        for detection in detections:
            landmark_string = (
                f"{repo.full_name}/{detection['filename']}, "
                f"PR #{pr.number} line {str(detection['line_number'])}"
            )

            image_source = "https://avatars.githubusercontent.com/u/48519090?s=30&v=4"
            logo = f"[![Logo]({image_source})]({APP_REPO})"
            body = "\n".join([
                f"### {logo} Suspicious code detected ###",
                f"**Detected:** {detection['message']}",
                f"**File:** {detection['filename']}",
                f"**Line:** {str(detection['line_number'])}",
                *[
                    f"**{key}:** {value}" for key, value in detection.items()
                    if key not in ['message', 'severity', 'line_number', 'filename']
                ]
            ])

            # Requires Repository Permissions: Pull requests -> Read and write
            comment = pr.create_review_comment(
                body=body,
                commit=repo.get_commit(pr.head.sha),
                path=detection['filename'],
                line=detection['line_number']
            )
            logger.info(
                f"Comment posted on {landmark_string}"
            )

    except KeyError as e:
        logger.error(
            f"Missing expected key in detection in {landmark_string}: {e}"
        )
    except ValueError as e:
        logger.error(
            f"Invalid value encountered while posting comment for {landmark_string}: {e}"
        )
    except GithubException as e:
        logger.error(
            f"GitHub API error commenting on {landmark_string}: {e}"
        )

    return comment


def create_commit_status(
    repo: Repository,
    commit_sha: str,
    status: str,
    description: str,
    target_url: str = 'https://github.com/apiiro/PRevent'
):
    try:
        commit = repo.get_commit(commit_sha)
        commit.create_status(
            context=SCAN_CONTEXT,
            state=status,
            description=description,
            target_url=target_url
        )
    except GithubException as e:
        logger.error(
            f"GitHub API error creating commit status for {commit_sha}: {e}"
        )
