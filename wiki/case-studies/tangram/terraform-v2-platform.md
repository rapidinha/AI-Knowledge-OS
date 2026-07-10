# Terraform v2 Platform (Tangram)

**When to use:** Read this case study when you need the concrete Tangram implementation behind terraform-v2 environment fan-out, module boundaries, secret handling, and lifecycle drift exceptions.

## Body

Tangram's `terraform-v2` stack uses one root module to compose staging and production from a shared `local.environments` map. The root creates shared KMS, certificate validation, Cloudflare zone lookup, internal DNS, and networking once, then fans out environment-scoped modules with `for_each` for database, storage, Cognito, SSM, ALB, SQS queues, ECS services, CI/CD, and event ingestion.

The backend is one S3 state key with DynamoDB locking. The README explicitly says both environments are managed by a single state, and `backend.tf` points to `tangram/production/terraform.tfstate`. This makes cross-environment drift visible in one plan, while increasing the review burden for every apply.

The root module is the integration layer. It wires database endpoints into SSM and ECS, Cognito outputs into ECS and Amplify, ALB target groups into ECS, SQS URLs and ARNs into ECS, Cloudflare records into ALB/Amplify/S3 endpoints, and New Relic configuration into ECS, Amplify, and the CloudWatch-to-Firehose log forwarding module.

Secrets enter through `.env`, not committed tfvars. The `./tf` wrapper refuses to run without `.env`, exports its values, then runs Terraform from the `terraform-v2` root. `.env.example` documents required `TF_VAR_*` names with placeholders for Cloudflare, GitHub, Asaas, New Relic, service API keys, Discord, Grafana, and other integrations. The stack then writes selected values into SSM SecureString parameters, Secrets Manager, ECS task environment variables, and module inputs.

Lifecycle drift exceptions are documented in the README and present in module code. Examples include generated Cognito Lambda artifacts, Discord bot task definitions, Asaas webhook Lambda environment values, SSM secret values, and Metabase scheduled scaling capacity. The runbook is to temporarily comment the lifecycle exception, plan/apply the intended change, then restore it.

## Trade-offs

- Tangram gets a single infrastructure plan that shows staging and production together.
- Shared modules keep networking, database, auth, ECS, ALB, queue, storage, DNS, and CI/CD boundaries recognizable.
- The single state expands blast radius because unrelated environment drift can appear during any apply.
- Local `.env` loading keeps secret setup simple, but operator machines must stay aligned and avoid committing real values.
- Lifecycle drift exceptions reduce noisy diffs, but they rely on humans following the documented temporary-unignore procedure.

## Anti-patterns

- Tangram avoids duplicating separate staging and production roots by driving most environment resources from `local.environments`.
- Tangram avoids committing real `.env` secrets, while keeping `terraform.tfvars` for public configuration.
- A current risk is relying on README module names or environment summaries without checking the root module, because some README claims diverge from the current Terraform code.
- A current risk is adding new `ignore_changes` entries without keeping the README table and change procedure current.

## Evidence

| Area | Path | Notes |
|------|------|-------|
| Architecture overview | `tangram-api-infra-prod/terraform-v2/README.md` | Shows Cloudflare, ALB, ECS Fargate, Amplify admin, S3 assets, n8n, Metabase, single-state environments, `.env` guidance, `./tf`, ignore_changes table, and New Relic note. |
| Remote state | `tangram-api-infra-prod/terraform-v2/backend.tf` | Configures one S3 backend key with DynamoDB locking and encryption. |
| Wrapper | `tangram-api-infra-prod/terraform-v2/tf` | Loads `.env`, exits if missing, changes to the terraform-v2 root, then runs Terraform. |
| Secret template | `tangram-api-infra-prod/terraform-v2/.env.example` | Documents placeholder `TF_VAR_*` values for tokens, API keys, capacity overrides, observability, and service-to-service credentials. |
| Environment fan-out | `tangram-api-infra-prod/terraform-v2/main.tf` | Defines staging/production settings and uses `for_each = local.environments` across database, storage, auth, SSM, ALB, SQS, ECS, CI/CD, and event modules. |
| Database and RDS Proxy | `tangram-api-infra-prod/terraform-v2/modules/database/main.tf` | Creates PostgreSQL, Redis, Secrets Manager credentials, optional RDS Proxy, target group, IAM role, and production protections. |
| Managed IdP | `tangram-api-infra-prod/terraform-v2/modules/auth/main.tf` | Creates Cognito user pool, web/backoffice/mobile clients, and SSM parameters for IDs and secrets. |
| Lambda lifecycle drift | `tangram-api-infra-prod/terraform-v2/modules/auth/lambda.tf` | Ignores generated Lambda package hash and filename drift. |
| Runtime secrets | `tangram-api-infra-prod/terraform-v2/modules/ssm/main.tf` | Stores database, Redis, JWT, Asaas, and service API-key values in parameters, with secret-value drift exceptions. |
| Application runtime | `tangram-api-infra-prod/terraform-v2/modules/ecs/main.tf` | Creates ECS cluster, logs, task roles, ECR repositories, SQS/KMS permissions, Cognito admin permissions, and per-service runtime wiring. |
| Routing | `tangram-api-infra-prod/terraform-v2/modules/alb/main.tf` | Creates ALB, HTTPS listener, per-service path rules, plus host rules for web frontend, n8n, and Metabase. |
| Queues | `tangram-api-infra-prod/terraform-v2/modules/sqs/main.tf` | Reusable queue module with optional DLQ, KMS encryption, redrive allow policy, and queue-depth alarm. |
| Olympiad queues | `tangram-api-infra-prod/terraform-v2/main.tf` | Instantiates olympiad import command, external orchestrator, and external students queues for each environment. |
| Hosted frontend CI | `tangram-api-infra-prod/terraform-v2/modules/amplify/main.tf` | Creates web and backoffice Amplify apps, main/staging branches, domain associations, and admin/backoffice environment variables. |
| DNS/CDN/WAF edge | `tangram-api-infra-prod/terraform-v2/modules/cloudflare/main.tf` | Creates API, app, admin, assets, automation, app-test, and BI records plus production SSL settings. |
| CI/CD | `tangram-api-infra-prod/terraform-v2/modules/cicd/main.tf` | Creates GitHub connection, artifact bucket, CodeBuild/CodePipeline roles, and deployment permissions. |
| Storage | `tangram-api-infra-prod/terraform-v2/modules/storage/main.tf` | Creates assets, olympiad artifacts, and VC imports buckets with encryption, CORS, policies, lifecycle, and task IAM policies. |
| New Relic logs | `tangram-api-infra-prod/terraform-v2/modules/newrelic-logs/main.tf` | Sends CloudWatch logs to New Relic through Lambda transformation, Firehose, backup S3, and log subscription filters. |
| Runtime scaling exception | `tangram-api-infra-prod/terraform-v2/modules/metabase/scheduling.tf` | Ignores scheduled scaling min/max capacity while scheduled actions change those values at runtime. |
| Capacity tuning | `tangram-api-infra-prod/terraform-v2/terraform.tfvars` | Captures service list, staging downscale, olympiad production sizing, repository IDs, and load-test-driven capacity comments. |

## Deviations

- The README environment table says production uses RDS Proxy, but `main.tf` currently passes `enable_rds_proxy = true` for every environment module instance. Treat the README as a summary and verify proxy scope against the root module before changing database connectivity.
- The README ignore_changes table names `modules/asaas-webhook/main.tf`, while the current root module instantiates `modules/asaas-events/main.tf`; that module contains the Lambda environment lifecycle exception.
- The README says the previous LGTM stack was removed in favor of New Relic, but `main.tf` still contains Grafana Cloud OTEL and deploy annotation inputs/modules. The extraction treats New Relic as the documented primary path and records Grafana references as remaining code paths.

## Principles

- [[principles/multi-env-terraform-single-state]] — Generalizes Tangram's staging/production fan-out from one remote state.
- [[principles/modular-iaas-boundaries]] — Generalizes Tangram's infrastructure module ownership model.
- [[principles/ignore-changes-and-secret-hygiene-in-iac]] — Generalizes Tangram's `.env`, sensitive variable, managed secret, and lifecycle drift practices.

## Related

- [[case-studies/tangram/identity-pbac-and-auth]]
- [[case-studies/tangram/index]]
- [[MOC/infrastructure]]
