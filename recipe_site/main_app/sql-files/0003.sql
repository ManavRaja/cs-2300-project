BEGIN;
--
-- Alter field name on customrecipe
--
ALTER TABLE "main_app_customrecipe" ADD CONSTRAINT "main_app_customrecipe_name_4d81f0d0_uniq" UNIQUE ("name");
CREATE INDEX "main_app_customrecipe_name_4d81f0d0_like" ON "main_app_customrecipe" ("name" varchar_pattern_ops);
--
-- Alter field name on premaderecipe
--
ALTER TABLE "main_app_premaderecipe" ADD CONSTRAINT "main_app_premaderecipe_name_35bd7fd8_uniq" UNIQUE ("name");
CREATE INDEX "main_app_premaderecipe_name_35bd7fd8_like" ON "main_app_premaderecipe" ("name" varchar_pattern_ops);
COMMIT;
