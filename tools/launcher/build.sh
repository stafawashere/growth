#!/bin/zsh
set -e

launcher_dir="${0:A:h}"
repo_root="${launcher_dir:h:h}"
app_path="${1:-/Applications/Growth.app}"
work_dir=$(mktemp -d)

trap 'rm -rf "$work_dir"' EXIT

"$repo_root/.venv/bin/python" "$launcher_dir/make_icon.py" "$work_dir/icon_1024.png"

mkdir -p "$work_dir/Growth.iconset"

for icon_size in 16 32 128 256 512; do
   retina_size=$((icon_size * 2))
   sips -z $icon_size $icon_size "$work_dir/icon_1024.png" --out "$work_dir/Growth.iconset/icon_${icon_size}x${icon_size}.png" >/dev/null
   sips -z $retina_size $retina_size "$work_dir/icon_1024.png" --out "$work_dir/Growth.iconset/icon_${icon_size}x${icon_size}@2x.png" >/dev/null
done

iconutil -c icns "$work_dir/Growth.iconset" -o "$work_dir/Growth.icns"

rm -rf "$app_path"
mkdir -p "$app_path/Contents/MacOS" "$app_path/Contents/Resources"

cp "$launcher_dir/Info.plist" "$app_path/Contents/Info.plist"
cp "$work_dir/Growth.icns" "$app_path/Contents/Resources/Growth.icns"
sed "s|__REPO_ROOT__|$repo_root|" "$launcher_dir/Growth" > "$app_path/Contents/MacOS/Growth"
chmod +x "$app_path/Contents/MacOS/Growth"

touch "$app_path"
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f "$app_path"

echo "built $app_path"
