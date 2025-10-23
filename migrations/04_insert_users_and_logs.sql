-- Insert Users
INSERT INTO "USER" (username, email, registration_date) VALUES
('benjamin_mccoy', 'benjamin_mccoy@outlook.com', '2024-01-11'),
('vivek_sharma', 'vivek_sharma@yahoo.com', '2024-02-14'),
('aryan_desai', 'aryan_desai@gmail.com', '2024-03-17'),
('mckenzie_tyler', 'mckenzie_tyler@gmail.com', '2024-04-20'),
('erick_melendez', 'erick_melendez@gmail.com', '2024-05-23'),
('emily_nguyen', 'emily_nguyen@gmail.com', '2024-06-26'),
('emmitt_pacheco', 'emmitt_pacheco@gmail.com', '2024-07-01'),
('fatima_khan', 'fatima_khan@outlook.com', '2024-08-04'),
('anjali_sharma', 'anjali_sharma@outlook.com', '2024-09-07'),
('maya_singh', 'maya_singh@gmail.com', '2024-10-10');

-- Insert Food Logs
INSERT INTO FOOD_INFO (user_id, food_id, log_date) VALUES
(1, 11, '2024-11-15'),  -- benjamin_mccoy ate food_id 11 on 2024-11-15
(1, 20, '2025-01-08'),  -- benjamin_mccoy ate food_id 20 on 2025-01-08
(1, 34, '2025-03-03'),  -- benjamin_mccoy ate food_id 34 on 2025-03-03
(1, 25, '2025-06-12'),  -- benjamin_mccoy ate food_id 25 on 2025-06-12
(1, 53, '2025-09-28'),  -- benjamin_mccoy ate food_id 53 on 2025-09-28
(1, 26, '2025-10-06'),  -- benjamin_mccoy ate food_id 26 on 2025-10-06

(2, 7,  '2024-12-02'),  -- vivek_sharma ate food_id 7 on 2024-12-02
(2, 8,  '2025-01-21'),  -- vivek_sharma ate food_id 8 on 2025-01-21
(2, 36, '2025-03-17'),  -- vivek_sharma ate food_id 36 on 2025-03-17
(2, 50, '2025-06-01'),  -- vivek_sharma ate food_id 50 on 2025-06-01
(2, 1,  '2025-08-19'),  -- vivek_sharma ate food_id 1 on 2025-08-19
(2, 4,  '2025-10-05'),  -- vivek_sharma ate food_id 4 on 2025-10-05

(3, 6,  '2024-11-22'),  -- aryan_desai ate food_id 6 on 2024-11-22
(3, 30, '2025-01-10'),  -- aryan_desai ate food_id 30 on 2025-01-10
(3, 2,  '2025-03-05'),  -- aryan_desai ate food_id 2 on 2025-03-05
(3, 28, '2025-06-20'),  -- aryan_desai ate food_id 28 on 2025-06-20
(3, 37, '2025-09-10'),  -- aryan_desai ate food_id 37 on 2025-09-10
(3, 52, '2025-10-06'),  -- aryan_desai ate food_id 52 on 2025-10-06

(4, 31, '2024-12-09'),  -- mckenzie_tyler ate food_id 31 on 2024-12-09
(4, 11, '2025-01-29'),  -- mckenzie_tyler ate food_id 11 on 2025-01-29
(4, 20, '2025-03-18'),  -- mckenzie_tyler ate food_id 20 on 2025-03-18
(4, 34, '2025-06-03'),  -- mckenzie_tyler ate food_id 34 on 2025-06-03
(4, 25, '2025-08-27'),  -- mckenzie_tyler ate food_id 25 on 2025-08-27
(4, 53, '2025-10-06'),  -- mckenzie_tyler ate food_id 53 on 2025-10-06

(5, 3,  '2024-11-28'),  -- erick_melendez ate food_id 3 on 2024-11-28
(5, 7,  '2025-01-06'),  -- erick_melendez ate food_id 7 on 2025-01-06
(5, 8,  '2025-03-01'),  -- erick_melendez ate food_id 8 on 2025-03-01
(5, 36, '2025-06-10'),  -- erick_melendez ate food_id 36 on 2025-06-10
(5, 50, '2025-09-05'),  -- erick_melendez ate food_id 50 on 2025-09-05
(5, 1,  '2025-10-06'),  -- erick_melendez ate food_id 1 on 2025-10-06

(6, 5,  '2024-12-14'),  -- emily_nguyen ate food_id 5 on 2024-12-14
(6, 6,  '2025-01-17'),  -- emily_nguyen ate food_id 6 on 2025-01-17
(6, 30, '2025-03-08'),  -- emily_nguyen ate food_id 30 on 2025-03-08
(6, 2,  '2025-06-15'),  -- emily_nguyen ate food_id 2 on 2025-06-15
(6, 28, '2025-09-22'),  -- emily_nguyen ate food_id 28 on 2025-09-22
(6, 37, '2025-10-06'),  -- emily_nguyen ate food_id 37 on 2025-10-06

(7, 18, '2024-11-19'),  -- emmitt_pacheco ate food_id 18 on 2024-11-19
(7, 31, '2025-01-22'),  -- emmitt_pacheco ate food_id 31 on 2025-01-22
(7, 11, '2025-03-14'),  -- emmitt_pacheco ate food_id 11 on 2025-03-14
(7, 20, '2025-06-07'),  -- emmitt_pacheco ate food_id 20 on 2025-06-07
(7, 34, '2025-09-01'),  -- emmitt_pacheco ate food_id 34 on 2025-09-01
(7, 25, '2025-10-06'),  -- emmitt_pacheco ate food_id 25 on 2025-10-06

(8, 26, '2024-12-01'),  -- fatima_khan ate food_id 26 on 2024-12-01
(8, 3,  '2025-01-12'),  -- fatima_khan ate food_id 3 on 2025-01-12
(8, 7,  '2025-03-09'),  -- fatima_khan ate food_id 7 on 2025-03-09
(8, 8,  '2025-06-18'),  -- fatima_khan ate food_id 8 on 2025-06-18
(8, 36, '2025-09-14'),  -- fatima_khan ate food_id 36 on 2025-09-14
(8, 50, '2025-10-06'),  -- fatima_khan ate food_id 50 on 2025-10-06

(9, 4,  '2024-11-30'),  -- anjali_sharma ate food_id 4 on 2024-11-30
(9, 5,  '2025-01-15'),  -- anjali_sharma ate food_id 5 on 2025-01-15
(9, 6,  '2025-03-11'),  -- anjali_sharma ate food_id 6 on 2025-03-11
(9, 30, '2025-06-22'),  -- anjali_sharma ate food_id 30 on 2025-06-22
(9, 2,  '2025-09-08'),  -- anjali_sharma ate food_id 2 on 2025-09-08
(9, 28, '2025-10-06'),  -- anjali_sharma ate food_id 28 on 2025-10-06

(10, 52, '2024-12-05'), -- maya_singh ate food_id 52 on 2024-12-05
(10, 18, '2025-01-24'), -- maya_singh ate food_id 18 on 2025-01-24
(10, 31, '2025-03-19'), -- maya_singh ate food_id 31 on 2025-03-19
(10, 11, '2025-06-05'), -- maya_singh ate food_id 11 on 2025-06-05
(10, 20, '2025-09-03'), -- maya_singh ate food_id 20 on 2025-09-03
(10, 34, '2025-10-06'); -- maya_singh ate food_id 34 on 2025-10-06
