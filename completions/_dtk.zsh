#compdef _dtk dtk

local line

_arguments -C \
    "-h[Show help information]" \
    "--help[Show help information]" \
    "1: :(maven docker helm k6 cleanup)" \
    "*::arg:->args"

case $line[1] in
maven)
    _dtk_maven
    ;;
docker)
    _dtk_docker
    ;;
helm)
    _dtk_helm
    ;;
k6)
    _dtk_k6
    ;;
cleanup)
    _dtk_cleanup
    ;;
esac

function _dtk_maven() {
    _arguments \
        "-h[show help]" \
        "1: :(clean install deploy sonar)" \
        "*::arg:->args"

    case $line[1] in
    clean)
        _dtk_maven_clean
        ;;
    install)
        _dtk_maven_install
        ;;
    deploy)
        _dtk_maven_deploy
        ;;
    sonar)
        _dtk_maven_sonar
        ;;
    esac
}

function _dtk_maven_clean() {
    _arguments \
        "-h[show help]"
}

function _dtk_maven_install() {
    _arguments \
        "-h[show help]" \
        "-m[module]" \
        "-s[skip test]"
}

function _dtk_maven_deploy() {
    _arguments \
        "-h[show help]" \
        "-s[skip test]"
}

function _dtk_maven_sonar() {
    _arguments \
        "-h[show help]" \
        "-t[run test]" \
        "-s[server]" \
        "-u[username]" \
        "-p[password]"
}

function _dtk_docker() {
    _arguments -C \
        "-h[Show help information]" \
        "1: :(images build push bpush login)" \
        "*::arg:->args"

    case $line[1] in
    images)
        _dtk_docker_images
        ;;
    build)
        _dtk_docker_build
        ;;
    push)
        _dtk_docker_push
        ;;
    bpush)
        _dtk_docker_bpush
        ;;
    login)
        _dtk_docker_login
        ;;
    esac
}

function _dtk_docker_images() {
    _arguments \
        "-h[show help]" \
        "-s[search for image]"
}

function _dtk_docker_build() {
    _arguments \
        "-h[show help]" \
        "-f[docker file]" \
        "-t[image tag:version]" \
        "-p[use public registry]"
}

function _dtk_docker_push() {
    _arguments \
        "-h[show help]" \
        "-t[image tag:version]" \
        "-p[use public registry]"
}

function _dtk_docker_bpush() {
    _arguments \
        "-h[show help]" \
        "-f[docker file]" \
        "-t[image tag:version]" \
        "-p[use public registry]"
}

function _dtk_docker_login() {
    _arguments \
        "-h[show help]" \
        "-i[internal (like harbor)]"
}

function _dtk_helm() {
    _arguments -C \
        "-h[Show help information]" \
        "1: :(list status deploy delete)" \
        "*::arg:->args"

    case $line[1] in
    list)
        _dtk_helm_list
        ;;
    status)
        _dtk_helm_status
        ;;
    deploy)
        _dtk_helm_deploy
        ;;
    delete)
        _dtk_helm_delete
        ;;
    esac
}

function _dtk_helm_list() {
    _arguments \
        "-h[show help]"
}

function _dtk_helm_status() {
    _arguments \
        "-h[show help]" \
        "-d[debug]" \
        "-s[show desc]" \
        "-n[namespace]"
}

function _dtk_helm_deploy() {
    _arguments \
        "-h[show help]" \
        "-f[values in a yaml file]" \
        "-s[secure]" \
        "-n[namespace]" \
        "-p[chart path]" \
        "-d[dry run]" \
        "-v[additional values]"
}

function _dtk_helm_delete() {
    _arguments \
        "-h[show help]"
}

function _dtk_k6() {
    _arguments -C \
        "-h[Show help information]" \
        "1: :(run)" \
        "*::arg:->args"

    case $line[1] in
    run)
        _dtk_k6_run
        ;;
    esac
}

function _dtk_k6_run() {
    _arguments \
        "-h[show help]" \
        "--ramp_up_duration[ramp up duration]" \
        "--ramp_max_duration[ramp max duration]" \
        "--ramp_down_duration[ramp down duration]" \
        "--max_users[max users]" \
        "--result_dir[result directory]" \
        "--result_file[result file]" \
        "--secure_url[secure url]" \
        "--api_gateway_url[api gateway url]" \
        "--username[username]" \
        "--password[password]" \
        "-v[verbose]"
}

function _dtk_cleanup() {
    _arguments \
        "-h[show help]" \
        "-i[intellij]" \
        "-n[npm]" \
        "-a[artifacts]" \
        "-d[docker]"
}
