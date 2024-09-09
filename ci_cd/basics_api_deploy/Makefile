ci_cd_file = "docker-compose-ci-cd.yaml"

up_api_deploy:
	docker compose -f $(ci_cd_file) stop basic-api-deploy
	docker compose -f $(ci_cd_file) rm -f basic-api-deploy
	docker compose -f $(ci_cd_file) up -d --no-deps --build --force-recreate basic-api-deploy
