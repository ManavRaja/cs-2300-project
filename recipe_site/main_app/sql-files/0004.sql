BEGIN;
--
-- Alter field name on customrecipe
--
DROP INDEX IF EXISTS "main_app_customrecipe_name_4d81f0d0_like";
--
-- Alter field name on premaderecipe
--
DROP INDEX IF EXISTS "main_app_premaderecipe_name_35bd7fd8_like";
--
-- Alter unique_together for customrecipe (1 constraint(s))
--
ALTER TABLE "main_app_customrecipe" ADD CONSTRAINT "main_app_customrecipe_user_id_name_3514bcd2_uniq" UNIQUE ("user_id", "name");
COMMIT;
