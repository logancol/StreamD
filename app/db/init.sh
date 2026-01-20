#!/bin/bash
set -euo pipefail

: "${ORACLE_RO_PASSWORD:?ORACLE_RO_PASSWORD is required}"
: "${APP_RW_PASSWORD:?APP_RW_PASSWORD is required}"
: "${AUTH_RO_PASSWORD:?AUTH_RO_PASSWORD is required}"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<SQL
DO \$\$
BEGIN
  CREATE USER oracle_ro WITH PASSWORD '${ORACLE_RO_PASSWORD}';
  CREATE USER auth_ro WITH PASSWORD '${AUTH_RO_PASSWORD}';
  CREATE USER app_rw WITH PASSWORD '${APP_RW_PASSWORD}';
END
\$\$;

ALTER ROLE oracle_ro SET default_transaction_read_only = on;
ALTER ROLE oracle_ro SET statement_timeout = '15s';
ALTER ROLE oracle_ro SET idle_in_transaction_session_timeout = '30s';

ALTER ROLE auth_ro SET default_transaction_read_only = on;
ALTER ROLE auth_ro SET statement_timeout = '15s';
ALTER ROLE auth_ro SET idle_in_transaction_session_timeout = '30s';
SQL