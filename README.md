# DeepGuard API

AI-generated voice detection API built for India AI Impact Buildathon 2026.

## Endpoint
POST /analyze

## Authentication
Header:
Authorization: deepguard123

## Input
Base64-encoded speech audio (mp3/wav)

## Output
- classification: AI_GENERATED or HUMAN
- confidence_score
- explanation

## Note
Designed for speech audio (calls, voice notes).

## Developer
team VigilAI
CSE-AIML Students
