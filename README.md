system_profiler SPHardwareDataType | grep "Hardware UUID"

curl -X POST https://c585-2001-861-5a80-43b0-8063-1977-1e7a-1aee.ngrok-free.app/generate \
-H "Content-Type: application/json" \
-d '{"machine_id": "2581C565-A188-5294-81B1-3C23B97333D0"}' -o apkg_generator
