#!/bin/bash

set -o errexit

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# ====================================
# Default variable
# ====================================
conda_installer=conda_installer.sh
is_init=false
is_create=false
is_install=false
is_package=false
is_update=false

# ====================================
# Read arguments
# ====================================
function print_usage() {
    cat <<USAGE
Usage: $0 [--conda-dir] [-c|-i|-p|-u] [-n <name>]
  --init               Initiate a new conda instance.
  --conda-dir          Conda directory.
  --python-version     Python version.
  -c, --create         Create a new conda environment.
  -e, --env            Environment to be created or updated. Default: axolpy.
  -i, --install        Install package from file.
  -p, --package        Package an environment.
  -u, --update         Update python library by loading python_library.txt in the same path of this script.
  -v, --version        Conda package version.
  -h, --help           Print this help.
USAGE
    exit
}

arguments=`getopt -o ce:i:puv:h --long init,conda-dir:,python-version:,create,env:,install:,package,update,version:,help -- "$@"`
eval set -- "${arguments}"

while true; do
    case "$1" in
        --init )
            is_init=true
            shift ;;
        --conda-dir )
            conda_dir="${2}"
            shift 2 ;;
        --python-version )
            python_version="${2}"
            shift 2 ;;
        -c | --create )
            is_create=true
            shift ;;
        -e | --env )
            env="${2}"
            shift 2 ;;
        -i | --install )
            is_install=true
            package_file="${2}"
            shift 2 ;;
        -p | --package )
            is_package=true
            shift ;;
        -u | --update )
            is_update=true
            shift ;;
        --version )
            version="${2}"
            shift 2 ;;
        -h | --help )
            print_usage
            shift ;;
        -- ) shift; break ;;
        * ) break ;;
    esac
done

! ${is_init} && ! ${is_create} && ! ${is_install} && ! ${is_package} && ! ${is_update} && print_usage

if ${is_init}; then
    echo ${conda_dir:?"--conda-dir is needed."} > /dev/null
    # You may replace the download url with your internal artifact repo to speed up
    # For stability, you may also download a fixed version instead of latest
    [ ! -f ${conda_installer} ] && wget -nv --output-document ${conda_installer} https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash ${conda_installer} -b -p ${conda_dir}
fi

echo ${conda_dir:=`which conda`} > /dev/null
conda_dir=${conda_dir/%\/bin\/conda/}
eval conda_dir=${conda_dir}
echo ${python_version:=3.5.2} > /dev/null
echo ${env:=axolpy} > /dev/null

if ${is_package}; then
    echo ${version:?"--version is needed."} > /dev/null
    ${conda_dir}/bin/conda package --name ${env} --pkg-name=${env} --pkg-version=${version}
    exit 0
fi

if ${is_create} || ${is_install} || ${is_update}; then
    if ${is_create}; then
        ${conda_dir}/bin/conda create --name ${env} python=${python_version} --yes
    fi

    source ${conda_dir}/bin/activate ${env}

    # Load a list of library to be updated in an environment
    if ${is_update}; then
        if [ -f "${DIR}/python_package.txt" ]; then
            while read lib ver; do
                if [ "$lib" != "#" ] && [ "$lib" != "" ]; then
                    # There is a compatibility issue when uninstalling setuptools in conda which causes 'Cannot remove entries from nonexistent file'.
                    # Adding --ignore-installed as a workaround.
                    # See https://github.com/pypa/pip/issues/2751 for detail.
                    /usr/bin/yes | pip install --upgrade --ignore-installed ${lib}==${ver}
                fi
            done < ${DIR}/python_package.txt
        fi

        if [ -f "${DIR}/conda_package.txt" ]; then
            while read lib ver; do
                if [ "$lib" != "#" ] && [ "$lib" != "" ]; then
                    ${conda_dir}/bin/conda install --yes ${lib}==${ver}
                fi
            done < ${DIR}/conda_package.txt
        fi
    fi

    if ${is_install}; then
        if [ -f ${package_file} ]; then
            pip install ${package_file}
        else
            echo "'${package_file}' is not found"
            exit 1
        fi
    fi
fi
