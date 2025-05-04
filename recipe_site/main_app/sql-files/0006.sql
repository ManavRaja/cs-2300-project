BEGIN;
--
-- Alter field recipes on weeklymealplan
--
ALTER TABLE "main_app_weeklymealplan_recipes" RENAME COLUMN "customrecipe_id" TO "premaderecipe_id";
COMMIT;
