#!/bin/bash

set -e

OUTPUT_FILE_PATH="./cryptek/test_and_check/"
COVERAGERC_FILE_PATH="${OUTPUT_FILE_PATH}.coveragerc"
COVERAGE_LOG_FILE="${OUTPUT_FILE_PATH}coverage.log"
LOG_FILE=${OUTPUT_FILE_PATH}"coverage.log"

# Display error messages and exit
function error_and_exit {
    echo "ERROR: $1"
    exit 1
}
function run_coverage {
    coverage erase || error_and_exit "Failed to clean up the old coverage files."
#     TODO: add a test report into the log file. Register the number of test failed, time, ect.
    coverage run --rcfile=$COVERAGERC_FILE_PATH manage.py test --timing|| error_and_exit "Tests failed. Cannot proceed."
    coverage run --rcfile=$COVERAGERC_FILE_PATH manage.py test --timing --reverse || error_and_exit "Tests failed. Cannot proceed."
    coverage run --rcfile=$COVERAGERC_FILE_PATH manage.py test --timing --shuffle || error_and_exit "Tests failed. Cannot proceed."
    coverage run --rcfile=$COVERAGERC_FILE_PATH  manage.py check
    coverage combine --quiet || error_and_exit "Failed to combine coverage data within the directory: $OUTPUT_FILE_PATH."
    COVERAGE_REPORT=$(coverage report --rcfile=$COVERAGERC_FILE_PATH || echo "The coverage report has FAILED.")
    coverage html  --directory=./cryptek/test_and_check/html_report --quiet || echo "Failed to generate HTML coverage report."
    coverage erase || error_and_exit "Failed to clean up the new coverage files."

    echo "${COVERAGE_REPORT}"
}
function run_check {
    local TAGS=(
        "admin" "caches" "compatibility" "files"
        "staticfiles" "templates" "translation"
        "models" "security" "database" "urls"
    )
    CHECK_OUTPUT=""
    for tag in "${TAGS[@]}"; do
        TAG_OUTPUT=$(python manage.py check --verbosity=3 --fail-level=WARNING --tag "$tag" 2>&1)
        if [[ "$TAG_OUTPUT" == *"System check identified no issues"* ]]; then
            CHECK_OUTPUT+="Check $tag: SUCCESS\n"
        else
            CHECK_OUTPUT+="Check $tag: ERROR\n$TAG_OUTPUT\n"
        fi
    done

    DEPLOY_OUTPUT=$(python manage.py check --deploy --verbosity=3 --fail-level=ERROR 2>&1)
    if [[ "$DEPLOY_OUTPUT" == *"System check identified no issues"* ]]; then
        CHECK_OUTPUT+="Check deploy: SUCCESS\n"
    else
        CHECK_OUTPUT+="Check deploy: ERROR\n$DEPLOY_OUTPUT\n"
    fi

    echo -e "$CHECK_OUTPUT"
}

# TODO: Write a Flake8 verification.
# TODO: Write a Isort verification.

# Generate or append log entry to a single log file# Generate or append log entry to a single log file
function generate_log_file {
    if [ ! -f "$LOG_FILE" ]; then
         echo "Log file $LOG_FILE does not exist. Creating a new log file."
         touch "$LOG_FILE" || error_and_exit "Failed to create log file $LOG_FILE."
    fi

    COVERAGE_SUMMARY=$(echo "$COVERAGE_REPORT" | grep TOTAL | awk '{print $4}' | sed 's/%//')

    local COVERAGE_PASSED="True"
    if echo "$COVERAGE_REPORT" | grep -qi "Coverage failure";
    then
        COVERAGE_PASSED="False"
    fi

    TOTAL_UNCOVERED_FILES=$(echo "$COVERAGE_REPORT" | awk '$6 > "0.00%" {count++} END {print count+1}')
    UNCOVERED_FILES=$(echo "$COVERAGE_REPORT" | awk '$6 == "0.00%" {count++} END {print count+0}')
    PARTIAL_UNCOVERED_FILES=$((TOTAL_UNCOVERED_FILES - UNCOVERED_FILES))
{
        echo "================= EXECUTION SUMMARY ================="
        echo "Execution Date: $(date "+%Y-%m-%d %H:%M:%S")"
        echo "Executed By: $USER"
        echo "------------- Django Checks --------------"
        echo -e "$1"
        echo "------------- Coverage Summary -----------"
        echo "Code Coverage: ${COVERAGE_SUMMARY:-0}%"
        echo "Uncovered Files: $TOTAL_UNCOVERED_FILES"
        echo "Total Uncovered Files: $UNCOVERED_FILES"
        echo "Partial Uncovered Files: $PARTIAL_UNCOVERED_FILES"
        echo "Coverage Passed: $COVERAGE_PASSED"
        echo "$COVERAGE_REPORT"
        echo "------------------------------------------------------------------------------------------------"
    } >> "$COVERAGE_LOG_FILE"
    echo "Log has been written to $COVERAGE_LOG_FILE"
}
# Main script execution
cd ../.. || error_and_exit "Failed to navigate to project root directory."

CHECK_OUTPUT=$(run_check)
run_coverage
generate_log_file "$CHECK_OUTPUT"
