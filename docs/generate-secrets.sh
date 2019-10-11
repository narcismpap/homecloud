# HomeCloud
# > Generate Secrets
#
# Author: Narcis.IO <n@narcis.io>

SECRETS=(
    'hc_db_root' \
    'hc_db_user' \
    'worker/hc_worker_code' \
    'worker/hc_worker_secret' \
)

if [ -d "runtime/secrets/" ]; then
    cd "runtime/secrets/"

    if [ ! -d "runtime/web" ]; then
        echo "runtime/web/ secrets directory does not exist"
        exit 100
    fi

    for scr in "${SECRETS[@]}"
    do
        echo "Generating ${scr}.txt"
        echo -n `openssl rand -base64 20 | tr -cd '[[:alnum:]]._-'` > "${scr}.txt"
    done

else
    echo "runtime/secrets/ directory does not exist. Are you in the right path?"
    exit 100
fi

