-- Populate the CATEGORY Table
INSERT INTO CATEGORY (category_name) VALUES
    ('Fruits'),
    ('Vegetables'),
    ('Proteins'),
    ('Grains'),
    ('Dairy'),
    ('Nuts & Seeds'),
    ('Beverages'),
    ('Snacks');

-- Populate the FOOD Table
INSERT INTO FOOD (food_name) VALUES
    -- Fruits (8)
    ('Apple'),
    ('Banana'),
    ('Orange'),
    ('Strawberry'),
    ('Grapes'),
    ('Watermelon'),
    ('Mango'),
    ('Blueberry'),

    -- Vegetables (8)
    ('Broccoli'),
    ('Carrot'),
    ('Spinach'),
    ('Tomato'),
    ('Cucumber'),
    ('Bell Pepper'),
    ('Lettuce'),
    ('Onion'),

    -- Proteins (10)
    ('Chicken Breast'),
    ('Salmon'),
    ('Ground Beef'),
    ('Eggs'),
    ('Tuna'),
    ('Pork Chop'),
    ('Turkey'),
    ('Shrimp'),
    ('Tofu'),
    ('Black Beans'),

    -- Grains (8)
    ('White Rice'),
    ('Brown Rice'),
    ('Wheat'),
    ('Oatmeal'),
    ('Quinoa'),
    ('Barley'),
    ('Millet'),
    ('Couscous'),

    -- Dairy (8)
    ('Whole Milk'),
    ('Cheddar Cheese'),
    ('Greek Yogurt'),
    ('Butter'),
    ('Mozzarella Cheese'),
    ('Cream Cheese'),
    ('Sour Cream'),
    ('Cottage Cheese'),

    -- Nuts & Seeds (8)
    ('Almonds'),
    ('Peanuts'),
    ('Cashews'),
    ('Walnuts'),
    ('Sunflower Seeds'),
    ('Chia Seeds'),
    ('Pumpkin Seeds'),
    ('Peanut Butter'),

    -- Beverages (6)
    ('Orange Juice'),
    ('Coffee'),
    ('Green Tea'),
    ('Almond Milk'),
    ('Soda'),
    ('Protein Shake'),

    -- Snacks (8)
    ('Potato Chips'),
    ('Chocolate Bar'),
    ('Granola Bar'),
    ('Popcorn'),
    ('Pretzels'),
    ('Trail Mix'),
    ('Crackers'),
    ('Energy Bar');


-- Populate the Belong_to Table
INSERT INTO Belong_to (food_id, category_id) VALUES
    -- Fruits (Category 1)
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (6, 1),
    (7, 1),
    (8, 1),

    -- Vegetables (Category 2)
    (9, 2),
    (10, 2),
    (11, 2),
    (12, 2),
    (13, 2),
    (14, 2),
    (15, 2),
    (16, 2),

    -- Proteins (Category 3)
    (17, 3),
    (18, 3),
    (19, 3),
    (20, 3),
    (21, 3),
    (22, 3),
    (23, 3),
    (24, 3),
    (25, 3),
    (26, 3),

    -- Grains (Category 4)
    (27, 4),
    (28, 4),
    (29, 4),
    (30, 4),
    (31, 4),
    (32, 4),
    (33, 4),
    (34, 4),

    -- Dairy (Category 5)
    (35, 5),
    (36, 5),
    (37, 5), 
    (38, 5),
    (39, 5),
    (40, 5),
    (41, 5),
    (42, 5),

    -- Nuts & Seeds (Category 6)
    (43, 6),
    (44, 6),
    (45, 6),
    (46, 6),
    (47, 6),
    (48, 6),
    (49, 6),
    (50, 6),

    -- Beverages (Category 7)
    (51, 7),
    (52, 7),
    (53, 7),
    (54, 7),
    (55, 7),
    (56, 7),

    -- Snacks (Category 8)
    (57, 8),
    (58, 8),
    (59, 8),
    (60, 8),
    (61, 8),
    (62, 8),
    (63, 8), 
    (64, 8);