#!/bin/bash

set -e

APP_NAME="QuikCap"
APP_BUNDLE="$APP_NAME.app"
DMG_NAME="$APP_NAME.dmg"
DIST_DIR="dist"

echo "🧹 Cleaning up previous builds..."
rm -rf "$DIST_DIR/$DMG_NAME" build __pycache__

if [ ! -d "$DIST_DIR/$APP_BUNDLE" ]; then
  echo "❌ Error: $DIST_DIR/$APP_BUNDLE not found."
  exit 1
fi

echo "📦 Creating DMG with create-dmg..."
create-dmg \
  --volname "$APP_NAME" \
  --window-size 500 300 \
  --icon "$APP_BUNDLE" 100 100 \
  --app-drop-link 350 100 \
  "$DIST_DIR/$DMG_NAME" \
  "$DIST_DIR/$APP_BUNDLE"

echo "✅ DMG created at: $DIST_DIR/$DMG_NAME"