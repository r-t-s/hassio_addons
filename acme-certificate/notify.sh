#!/bin/bash
curl -X POST -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" -H "Content-Type: application/json" -d "{\"message\" : \"Certificates Updated: ${DEPLOY_TARGET}\", \"title\" : \"Reboot Needed\", \"notification_id\": \"${DEPLOY_TARGET}\"}" http://supervisor/core/api/services/persistent_notification/create
