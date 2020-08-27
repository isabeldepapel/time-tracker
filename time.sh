#!/bin/bash

ENVS=("integ" "us" "emea" "pscc")
OPS=("apply" "build")

to_upper() {
    echo $(echo "$1" | tr '[:lower:]' '[:upper:]')
}

# takes env name, op, and kind (start or end) as params
generate_var_name() {
    local env="$1"
    local op="$2"
    local kind="$3"

    echo "$(to_upper "$env")_$(to_upper "$op")_$(to_upper "$kind")"
}

validate_env() {
    local env="$1"

    if [ -z "${env}" ]; then
        echo "specify env"
        exit 1
    elif [[ ! " ${ENVS[@]} " =~ " ${env} " ]]; then
        echo "invalid env: ${env}"
        exit 1
    fi
    echo "valid env"
}

validate_op() {
    local op="$1"

    if [ -z "${op}" ]; then
        echo "specify op"
        exit 1
    elif [[ ! " ${OPS[@]} " =~ " ${op} " ]]; then
        echo "invalid op: ${op}"
        exit 1
    fi
    echo "valid op"
}

# export datetime to a given env var based on op, env, and kind (start or end)
export_datetime() {
    local datetime=$(date +%s%6N) # get 6 most significant digits
    local op="$1"
    local env="$2"
    local kind="$3"

    validate_op "$op"
    validate_env "$env"

    local var_name=$(generate_var_name "$env" "$op" "$kind")
    local env_var="$var_name=$datetime"

    echo $env_var
    export $env_var
}

start_time() {
    local op="$1"
    local env="$2"

    export_datetime "$op" "$env" "start"
}

end_time() {
    local op="$1"
    local env="$2"
    local num_builds="$3"

    export_datetime "$op" "$env" "end"
    write_to_notion "$op" "$env" "$num_builds"
}

write_to_notion() {
    local op="$1"
    local env="$2"
    local num_builds="$3"

    local start_var_name=$(generate_var_name "$env" "$op" "start")
    local end_var_name=$(generate_var_name "$env" "$op" "end")

    python time.py "$op" "$env" "$num_builds"
}

main() {
    command="$1"
    case $command in
        "start")
            shift
            start_time "$@"
            ;;
        "end")
            shift
            end_time "$@"
            ;;
        "write-data")
            shift
            write_to_notion "$@"
            ;;
        *)
            exit 1
            ;;
    esac
}

main "$@"
