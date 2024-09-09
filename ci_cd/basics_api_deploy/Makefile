ci_cd_file = "docker-compose-ci-test.yml"

up_api_deploy:
	docker compose -f $(ci_cd_file) stop api
	docker compose -f $(ci_cd_file) rm -f api
	docker compose -f $(ci_cd_file) up -d --no-deps --build --force-recreate basic-api-deploy
