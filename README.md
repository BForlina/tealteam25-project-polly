# Polly → S3 CI/CD Example

This repo demonstrates a GitHub-based CI/CD pipeline that:
- Converts `speech.txt` to an MP3 using Amazon Polly.
- Uploads the MP3 to an S3 bucket under the prefix `polly-audio/`.
- Uses two GitHub Actions workflows:
  - `on_pull_request.yml` — runs on PRs to `main` and writes `polly-audio/beta.mp3`
  - `on_merge.yml` — runs on pushes to `main` and writes `polly-audio/prod.mp3`

---

## Files of interest
- `speech.txt` — sample text to synthesize.
- `synthesize.py` — script that calls Amazon Polly and uploads to S3 (reads configuration from environment variables).
- `.github/workflows/on_pull_request.yml` — PR workflow (beta).
- `.github/workflows/on_merge.yml` — main branch workflow (prod).

---

## Setup: AWS & S3
1. Create an S3 bucket (e.g., `my-polly-bucket`) in your chosen region.
2. Ensure the IAM principal (user/role) used by GitHub Actions has:
   - `polly:SynthesizeSpeech`
   - `s3:PutObject` permission for `arn:aws:s3:::<your-bucket>/polly-audio/*`
   (See `polly-policy.json` example in repo)

---

## Setup: GitHub repository secrets
In the GitHub repo, add these secrets (Settings → Secrets → Actions):
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION` (e.g. `us-east-1`)
- `S3_BUCKET` (your bucket name)

**Tip:** Use GitHub OIDC with a short-lived role for better security (not shown here).

---

## How to modify the text
Edit `speech.txt` in the repo and commit. For local tests, change `TEXT_FILE` env var or edit the file contents.

---

## How to trigger workflows
- **PR**: Open a PR targeting `main` — `on_pull_request.yml` will run and write `polly-audio/beta.mp3`.
- **Merge**: Merge the PR to `main` (or push directly to `main`) — `on_merge.yml` will run and write `polly-audio/prod.mp3`.

---

## How to verify uploaded .mp3 files
1. AWS Console:
   - Go to S3 → your bucket → `polly-audio/` and check `beta.mp3` / `prod.mp3`.
2. AWS CLI example:
   ```bash
   aws s3 ls s3://YOUR_BUCKET_NAME/polly-audio/
   aws s3 cp s3://YOUR_BUCKET_NAME/polly-audio/prod.mp3 ./prod.mp3

