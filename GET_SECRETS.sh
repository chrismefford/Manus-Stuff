#!/bin/bash
# Script to extract the values you need for GitHub Secrets

echo "================================================================================"
echo "GITHUB SECRETS VALUES"
echo "================================================================================"
echo ""
echo "Copy these values to your GitHub repository secrets:"
echo ""
echo "--------------------------------------------------------------------------------"
echo "SECRET 1: OPENAI_API_KEY"
echo "--------------------------------------------------------------------------------"
echo "$OPENAI_API_KEY"
echo ""
echo "--------------------------------------------------------------------------------"
echo "SECRET 2: GOOGLE_CREDENTIALS"
echo "--------------------------------------------------------------------------------"
cat /home/ubuntu/credentials.json
echo ""
echo ""
echo "--------------------------------------------------------------------------------"
echo "SECRET 3: GOOGLE_TOKEN"
echo "--------------------------------------------------------------------------------"
cat /home/ubuntu/token.json
echo ""
echo ""
echo "================================================================================"
echo "Next steps:"
echo "1. Go to your GitHub repository → Settings → Secrets and variables → Actions"
echo "2
