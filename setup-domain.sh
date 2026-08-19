#!/usr/bin/env bash
# Point scarab.quest at this GitHub Pages site.
#
# Run this only AFTER you own the domain and have added the DNS records below at
# your registrar. Setting the custom domain before DNS resolves makes GitHub
# redirect the working github.io URL to a domain that isn't answering yet.
#
#   Type   Name   Value
#   A      @      185.199.108.153
#   A      @      185.199.109.153
#   A      @      185.199.110.153
#   A      @      185.199.111.153
#   CNAME  www    kevinmchan.github.io.
#
set -euo pipefail

DOMAIN="${1:-scarab.quest}"
REPO="kevinmchan/scarab"

echo "Checking DNS for $DOMAIN ..."
GITHUB_IPS="185.199.108.153 185.199.109.153 185.199.110.153 185.199.111.153"
RESOLVED="$(dig +short "$DOMAIN" A || true)"
if [ -z "$RESOLVED" ]; then
  echo "  ✗ $DOMAIN has no A records yet. Add the records above, wait for them to"
  echo "    propagate (usually minutes, up to an hour), then run this again."
  exit 1
fi
MATCHED=0
for ip in $RESOLVED; do
  case " $GITHUB_IPS " in *" $ip "*) MATCHED=1 ;; esac
done
if [ "$MATCHED" -eq 0 ]; then
  echo "  ✗ $DOMAIN resolves to: $RESOLVED"
  echo "    None of those are GitHub Pages addresses. Check the A records."
  exit 1
fi
echo "  ✓ DNS points at GitHub Pages"

echo "Setting the custom domain on $REPO ..."
gh api -X PUT "repos/$REPO/pages" -f "cname=$DOMAIN" >/dev/null
echo "  ✓ custom domain set"

echo "Waiting for the HTTPS certificate (this can take a few minutes) ..."
for i in $(seq 1 40); do
  if gh api "repos/$REPO/pages" --jq '.https_certificate.state' 2>/dev/null | grep -q approved; then
    gh api -X PUT "repos/$REPO/pages" -F "https_enforced=true" >/dev/null || true
    echo "  ✓ certificate issued, HTTPS enforced"
    break
  fi
  sleep 15
done

echo
echo "Done. The game is at https://$DOMAIN"
echo "Share links now read https://$DOMAIN/#r=CODE — the page builds them from"
echo "whatever address it is served on, so nothing else needs changing."
