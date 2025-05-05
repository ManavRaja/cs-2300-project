BEGIN;
--
-- Alter field name on customrecipe
--
ALTER TABLE "main_app_customrecipe" ALTER COLUMN "name" SET DEFAULT 'My Recipe Name';
UPDATE "main_app_customrecipe" SET "name" = 'My Recipe Name' WHERE "name" IS NULL; SET CONSTRAINTS ALL IMMEDIATE;
ALTER TABLE "main_app_customrecipe" ALTER COLUMN "name" SET NOT NULL;
ALTER TABLE "main_app_customrecipe" ALTER COLUMN "name" DROP DEFAULT;
--
-- Alter field name on premaderecipe
--
ALTER TABLE "main_app_premaderecipe" ALTER COLUMN "name" SET DEFAULT 'My Recipe Name';
UPDATE "main_app_premaderecipe" SET "name" = 'My Recipe Name' WHERE "name" IS NULL; SET CONSTRAINTS ALL IMMEDIATE;
ALTER TABLE "main_app_premaderecipe" ALTER COLUMN "name" SET NOT NULL;
ALTER TABLE "main_app_premaderecipe" ALTER COLUMN "name" DROP DEFAULT;
COMMIT;
