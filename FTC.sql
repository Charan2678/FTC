-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 06, 2022 at 09:56 AM
-- Server version: 10.4.20-MariaDB
-- PHP Version: 7.3.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `efarming_portal`
--

-- --------------------------------------------------------

--
-- Table structure for table `company`
--

CREATE TABLE `company` (
  `company_id` int(11) NOT NULL,
  `company_name` varchar(255) NOT NULL,
  `company_description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `company`
--

INSERT INTO `company` (`company_id`, `company_name`, `company_description`) VALUES
(1, 'Agricutural', ''),
(2, 'Lettuce', ''),
(3, 'Tata', ''),
(4, 'BPB', '');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('1yszxy97tw2qhvxtkfzcipmqmxg5901o', 'OTJjZGRkY2E5ZjhhZDYwOTczNTQxZDlkNTJhNTYzNGY5ZDRjMDgwMjp7InVzZXJfaWQiOjgsInVzZXJfbGV2ZWxfaWQiOjEsImF1dGhlbnRpY2F0ZWQiOnRydWUsInVzZXJfbmFtZSI6IkFtaXQgS3VtYXIifQ==', '2018-01-26 07:59:01'),
('9bgzvan3fd73sdzjqy4fy90dxwzgmltg', 'MDZiNTU1MGVjZDFkNDliNDc3ZWY1OGExZDgwOTk5MWFkYTZjZmE3NDp7ImF1dGhlbnRpY2F0ZWQiOmZhbHNlLCJ1c2VyX2xldmVsX2lkIjpmYWxzZSwidXNlcl9pZCI6ZmFsc2UsInVzZXJfbmFtZSI6ZmFsc2V9', '2018-01-29 14:09:38'),
('c7f2yysow67qjgtrgzabr8rx8eyvdnji', 'MDZiNTU1MGVjZDFkNDliNDc3ZWY1OGExZDgwOTk5MWFkYTZjZmE3NDp7ImF1dGhlbnRpY2F0ZWQiOmZhbHNlLCJ1c2VyX2xldmVsX2lkIjpmYWxzZSwidXNlcl9pZCI6ZmFsc2UsInVzZXJfbmFtZSI6ZmFsc2V9', '2018-01-29 14:19:42'),
('ebqsosvupih3d6rfcy220w6eeoopoqt8', 'NDE1ODNmMjY1ZjNlZDA2Y2ExYzc1ZGU5NWEyNGEzN2IzMWY2OGVjYTp7Im9yZGVyX2lkIjoiMCIsImF1dGhlbnRpY2F0ZWQiOmZhbHNlLCJ1c2VyX2xldmVsX2lkIjpmYWxzZSwidXNlcl9pZCI6ZmFsc2UsInVzZXJfbmFtZSI6ZmFsc2V9', '2018-02-21 10:22:08'),
('j1unuxzc2z846m0r1xmkioa3xd63spfg', 'ODFkZmU0YjE3MzI5ODQ5NzQyNzc4Nzc0ODNjZjlkYTlhZWEwMmMxOTp7InVzZXJfaWQiOjI1LCJ1c2VyX2xldmVsX2lkIjoyLCJhdXRoZW50aWNhdGVkIjp0cnVlLCJ1c2VyX25hbWUiOiJLYXVzaGFsIEtpc2hvcmUifQ==', '2018-02-21 09:19:01'),
('pm9ifc6usfn38cwfcpuget8cu0g48c3k', 'OTJjZGRkY2E5ZjhhZDYwOTczNTQxZDlkNTJhNTYzNGY5ZDRjMDgwMjp7InVzZXJfaWQiOjgsInVzZXJfbGV2ZWxfaWQiOjEsImF1dGhlbnRpY2F0ZWQiOnRydWUsInVzZXJfbmFtZSI6IkFtaXQgS3VtYXIifQ==', '2018-01-29 13:36:24'),
('po0ih0jpd5jzt8r4yjplf56fut88l2bz', 'OGQwNWU0ZWZmZWFkN2UxODYzMzQyY2UyY2ZiMzNmOWMxNDU4NWVkMjp7ImF1dGhlbnRpY2F0ZWQiOmZhbHNlLCJ1c2VyX2lkIjpmYWxzZSwidXNlcl9sZXZlbF9pZCI6ZmFsc2UsInVzZXJfbmFtZSI6ZmFsc2V9', '2022-07-20 07:56:28'),
('qi4jui1wag7y5kjd3nal07b1h2jlc9ia', 'OTJjZGRkY2E5ZjhhZDYwOTczNTQxZDlkNTJhNTYzNGY5ZDRjMDgwMjp7InVzZXJfaWQiOjgsInVzZXJfbGV2ZWxfaWQiOjEsImF1dGhlbnRpY2F0ZWQiOnRydWUsInVzZXJfbmFtZSI6IkFtaXQgS3VtYXIifQ==', '2017-07-21 11:40:27'),
('xqitzy5mm8bz740ja8unqi2yzmdyj7ed', 'MDMwNWRjNWZmMGI3MjYyOWE1ZDI2YjE1NWEzMjg3OWVkYzM3MjEwNDp7Im9yZGVyX2lkIjozNCwiYXV0aGVudGljYXRlZCI6ZmFsc2UsInVzZXJfbGV2ZWxfaWQiOmZhbHNlLCJ1c2VyX2lkIjpmYWxzZSwidXNlcl9uYW1lIjpmYWxzZX0=', '2018-02-20 13:24:04');

-- --------------------------------------------------------

--
-- Table structure for table `order`
--

CREATE TABLE `order` (
  `order_id` int(11) NOT NULL,
  `order_user_id` varchar(255) NOT NULL,
  `order_date` varchar(255) NOT NULL,
  `order_status` varchar(255) NOT NULL,
  `order_total` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `order`
--

INSERT INTO `order` (`order_id`, `order_user_id`, `order_date`, `order_status`, `order_total`) VALUES
(1, '25', '01:49PM on February 06, 2018', '2', '0'),
(2, '25', '01:50PM on February 06, 2018', '5', '0'),
(3, '25', '04:06PM on February 06, 2018', '5', '0'),
(4, '25', '09:19AM on February 07, 2018', '5', '0');

-- --------------------------------------------------------

--
-- Table structure for table `order_item`
--

CREATE TABLE `order_item` (
  `oi_id` int(11) NOT NULL,
  `oi_order_id` varchar(255) NOT NULL,
  `oi_product_id` varchar(255) NOT NULL,
  `oi_price_per_unit` varchar(255) NOT NULL,
  `oi_cart_quantity` varchar(255) NOT NULL,
  `oi_total` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `order_item`
--

INSERT INTO `order_item` (`oi_id`, `oi_order_id`, `oi_product_id`, `oi_price_per_unit`, `oi_cart_quantity`, `oi_total`) VALUES
(1, '1', '7', '1200', '1', '1200'),
(2, '1', '8', '1200', '1', '1200'),
(3, '2', '6', '1170', '1', '1170'),
(4, '2', '2', '1100', '1', '1100'),
(5, '2', '3', '1170', '4', '4680'),
(6, '3', '8', '1200', '1', '1200'),
(7, '4', '1', '1200', '1', '1200'),
(8, '4', '5', '1170', '1', '1170'),
(9, '4', '7', '1200', '2', '2400'),
(10, '4', '9', '3423', '1', '3423');

-- --------------------------------------------------------

--
-- Table structure for table `order_status`
--

CREATE TABLE `order_status` (
  `os_id` int(11) NOT NULL,
  `os_title` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `order_status`
--

INSERT INTO `order_status` (`os_id`, `os_title`) VALUES
(1, 'Confirmed'),
(2, 'Processing'),
(3, 'Packed'),
(4, 'Dispatched'),
(5, 'Cancelled');

-- --------------------------------------------------------

--
-- Table structure for table `products_product`
--

CREATE TABLE `products_product` (
  `product_id` int(11) NOT NULL,
  `product_vendor_id` varchar(255) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `product_type_id` varchar(255) NOT NULL,
  `product_company_id` varchar(255) NOT NULL,
  `product_price` varchar(255) NOT NULL,
  `product_image` varchar(255) NOT NULL,
  `product_description` text NOT NULL,
  `product_stock` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `products_product`
--

INSERT INTO `products_product` (`product_id`, `product_vendor_id`, `product_name`, `product_type_id`, `product_company_id`, `product_price`, `product_image`, `product_description`, `product_stock`) VALUES
(1, '1002', 'Kobyashi', '2', '1', '1200', '/uploads/kobyashi seeds.jpeg', 'Seed is the most important and vital input for agricultural production. ... It is, therefore, important that quality seeds are made available to the farmers of the country. The Indian Seeds programme recognizes three generations of seeds, namely, breeder, foundation and certified seeds.', '5'),
(2, '1002', 'Home Farming', '1', '1', '1100', '/uploads/home farming Seeds.jpeg', 'Seed is the most important and vital input for agricultural production. ... It is, therefore, important that quality seeds are made available to the farmers of the country. The Indian Seeds programme recognizes three generations of seeds, namely, breeder, foundation and certified seeds.', '91'),
(3, '1002', 'Gralic Seeds', '4', '2', '199', '/uploads/garlic seeds.jpeg', 'Seed is the most important and vital input for agricultural production. ... It is, therefore, important that quality seeds are made available to the farmers of the country. The Indian Seeds programme recognizes three generations of seeds, namely, breeder, foundation and certified seeds.', '199'),
(4, '1017', 'Seeds Medicine', '4', '1', '240', '/uploads/Insecticides Medicine.jpeg', 'Seed is the most important and vital input for agricultural production. ... It is, therefore, important that quality seeds are made available to the farmers of the country. The Indian Seeds programme recognizes three generations of seeds, namely, breeder, foundation and certified seeds.', '87'),
(5, '1017', 'Hybrid Seeds', '1', '3', '350', '/uploads/hybrid seeds.jpeg', 'Seed is the most important and vital input for agricultural production. ... It is, therefore, important that quality seeds are made available to the farmers of the country. The Indian Seeds programme recognizes three generations of seeds, namely, breeder, foundation and certified seeds.', '12'),
(6, '1018', 'Vegetable Seeds', '2', '1', '1170', '/uploads/vegetable seed.jpeg', 'Seed is the most important and vital input for agricultural production. ... It is, therefore, important that quality seeds are made available to the farmers of the country. The Indian Seeds programme recognizes three generations of seeds, namely, breeder, foundation and certified seeds.', '15'),
(7, '1018', 'Vitamin Seeds', '2', '3', '1200', '/uploads/Vitamin Seeds.jpeg', 'Seed is the most important and vital input for agricultural production. ... It is, therefore, important that quality seeds are made available to the farmers of the country. The Indian Seeds programme recognizes three generations of seeds, namely, breeder, foundation and certified seeds.', '97'),
(8, '1017', 'Jute Orgainc', '1', '2', '250', '/uploads/jute organic.jpeg', 'Seed is the most important and vital input for agricultural production. ... It is, therefore, important that quality seeds are made available to the farmers of the country. The Indian Seeds programme recognizes three generations of seeds, namely, breeder, foundation and certified seeds.', '100'),
(9, '1001', 'Grain Seeds', '3', '2', '342', '/uploads/grain.jpeg', 'Seed is the most important and vital input for agricultural production. ... It is, therefore, important that quality seeds are made available to the farmers of the country. The Indian Seeds programme recognizes three generations of seeds, namely, breeder, foundation and certified seeds.', '32'),
(10, '1018', 'Zukur Seeds', '3', '3', '300', '/uploads/zukur seeds.jpeg', 'Seed is the most important and vital input for agricultural production. ... It is, therefore, important that quality seeds are made available to the farmers of the country. The Indian Seeds programme recognizes three generations of seeds, namely, breeder, foundation and certified seeds.', '23');

-- --------------------------------------------------------

--
-- Table structure for table `type`
--

CREATE TABLE `type` (
  `type_id` int(11) NOT NULL,
  `type_name` varchar(255) NOT NULL,
  `type_description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `type`
--

INSERT INTO `type` (`type_id`, `type_name`, `type_description`) VALUES
(1, 'Flower Seeds', 'Computer'),
(2, 'Vegetable Seeds', 'Maths'),
(3, 'Grain Seeds', 'CBSE'),
(4, 'Organic Seeds\r\n', 'UGC');

-- --------------------------------------------------------

--
-- Table structure for table `users_city`
--

CREATE TABLE `users_city` (
  `city_id` int(11) NOT NULL,
  `city_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `users_city`
--

INSERT INTO `users_city` (`city_id`, `city_name`) VALUES
(1, 'Allahabad'),
(2, 'Varanasi');

-- --------------------------------------------------------

--
-- Table structure for table `users_country`
--

CREATE TABLE `users_country` (
  `country_id` int(11) NOT NULL,
  `country_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `users_country`
--

INSERT INTO `users_country` (`country_id`, `country_name`) VALUES
(1, 'India'),
(2, 'USA');

-- --------------------------------------------------------

--
-- Table structure for table `users_role`
--

CREATE TABLE `users_role` (
  `role_id` int(11) NOT NULL,
  `role_title` varchar(255) NOT NULL,
  `role_description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users_role`
--

INSERT INTO `users_role` (`role_id`, `role_title`, `role_description`) VALUES
(1, 'System Admin', 'Admin Roles and Permissions'),
(2, 'Normal User', 'Users Roles and Permissions'),
(3, 'Doctor', 'Doctors User Permission and Role'),
(4, 'Patient', 'Patient User Permission and Role');

-- --------------------------------------------------------

--
-- Table structure for table `users_state`
--

CREATE TABLE `users_state` (
  `state_id` int(11) NOT NULL,
  `state_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users_state`
--

INSERT INTO `users_state` (`state_id`, `state_name`) VALUES
(1, 'UttarnPradesh'),
(2, 'Madhya Pradesh');

-- --------------------------------------------------------

--
-- Table structure for table `users_user`
--

CREATE TABLE `users_user` (
  `user_id` int(11) NOT NULL,
  `user_level_id` int(11) NOT NULL DEFAULT 2,
  `user_username` varchar(255) NOT NULL,
  `user_password` varchar(255) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `user_add1` varchar(255) NOT NULL,
  `user_add2` varchar(255) NOT NULL,
  `user_city` int(11) NOT NULL,
  `user_state` int(11) NOT NULL,
  `user_country` int(11) NOT NULL,
  `user_email` varchar(255) NOT NULL,
  `user_mobile` varchar(255) NOT NULL,
  `user_gender` varchar(255) NOT NULL,
  `user_dob` varchar(255) NOT NULL,
  `user_image` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `users_user`
--

INSERT INTO `users_user` (`user_id`, `user_level_id`, `user_username`, `user_password`, `user_name`, `user_add1`, `user_add2`, `user_city`, `user_state`, `user_country`, `user_email`, `user_mobile`, `user_gender`, `user_dob`, `user_image`) VALUES
(8, 1, 'admin', 'test', 'Amit Kumar', 'Allahabad', 'Lunckonw', 1, 1, 1, 'amit@gmail.com', '9878987678', 'Male', '2 July,1987', '/uploads/p1.jpg'),
(10, 1, 'manasa', 'test', 'Manasa Singh', 'House no : 768', 'Noida', 2, 1, 1, 'manasa@gmail.com', '9876543212', 'Female', '18 January,1968', '/uploads/p2.jpg'),
(11, 2, 'aman', 'test', 'Aman Kumar', 'House No : 355, Sector 23', 'Noida', 1, 2, 1, 'aman@gmail.com', '987654321', 'Male', '18 January,1968', '/uploads/p3.jpg'),
(14, 2, 'pawan', 'test', 'Pawan Kumar', 'House No : 355, Sector 23', 'Noida', 1, 1, 2, 'pawan@gmail.com', '987654321', 'Male', '18 January,1968', '/uploads/p5.jpg'),
(15, 3, 'vishal', 'test', 'Vishal Singh', 'House No : 355, Sector 23', 'Noida', 1, 1, 2, 'vvishal@gmail.com', '987654321', 'Male', '18 January,1968', '/uploads/d1.jpg'),
(16, 3, 'admin1', 'test', 'Amit Kumar', 'Allahabad', 'Lunckonw', 1, 1, 1, 'amit@gmail.com', '9878987678', 'Male', '2 July,1987', '/uploads/d2.jpg'),
(17, 3, 'manasa', 'test', 'Manasa Singh', 'House no : 768', 'Noida', 2, 1, 1, 'manasa@gmail.com', '9876543212', 'Female', '18 January,1968', '/uploads/d3.jpg'),
(18, 3, 'aman', 'test', 'Aman Kumar', 'House No : 355, Sector 23', 'Noida', 1, 2, 1, 'aman@gmail.com', '987654321', 'Male', '18 January,1968', '/uploads/d4.jpg'),
(19, 4, 'kaushal', 'test', 'Kaushal Kishore', 'House No : 355, Sector 23', 'Noida', 2, 2, 2, 'kaushal@gmail.com', '987654321', 'Male', '18 January,1968', '/uploads/p6.jpg'),
(20, 4, 'pawan', 'test', 'Pawan Kumar', 'House No : 355, Sector 23', 'Noida', 1, 1, 2, 'pawan@gmail.com', '987654321', 'Male', '18 January,1968', '/uploads/p7.jpg'),
(21, 4, 'vishal', 'test', 'Vishal Singh', 'House No : 355, Sector 23', 'Noida', 1, 1, 2, 'vvishal@gmail.com', '987654321', 'Male', '18 January,1968', '/uploads/p8.jpg'),
(25, 2, 'customer', 'test', 'Kaushal Kishore', 'S  206 Amrapali Zodiac', 'Sector 120 Noida', 1, 2, 1, 'kaushal.rahuljaiswal@gmail.com', '8376986802', 'Male', '12 February,2018', '/uploads/28bdc83.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `company`
--
ALTER TABLE `company`
  ADD PRIMARY KEY (`company_id`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`order_id`);

--
-- Indexes for table `order_item`
--
ALTER TABLE `order_item`
  ADD PRIMARY KEY (`oi_id`);

--
-- Indexes for table `order_status`
--
ALTER TABLE `order_status`
  ADD PRIMARY KEY (`os_id`);

--
-- Indexes for table `products_product`
--
ALTER TABLE `products_product`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `type`
--
ALTER TABLE `type`
  ADD PRIMARY KEY (`type_id`);

--
-- Indexes for table `users_city`
--
ALTER TABLE `users_city`
  ADD PRIMARY KEY (`city_id`);

--
-- Indexes for table `users_country`
--
ALTER TABLE `users_country`
  ADD PRIMARY KEY (`country_id`);

--
-- Indexes for table `users_role`
--
ALTER TABLE `users_role`
  ADD PRIMARY KEY (`role_id`);

--
-- Indexes for table `users_state`
--
ALTER TABLE `users_state`
  ADD PRIMARY KEY (`state_id`);

--
-- Indexes for table `users_user`
--
ALTER TABLE `users_user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `company`
--
ALTER TABLE `company`
  MODIFY `company_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `order`
--
ALTER TABLE `order`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `order_item`
--
ALTER TABLE `order_item`
  MODIFY `oi_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `order_status`
--
ALTER TABLE `order_status`
  MODIFY `os_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `products_product`
--
ALTER TABLE `products_product`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `type`
--
ALTER TABLE `type`
  MODIFY `type_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users_city`
--
ALTER TABLE `users_city`
  MODIFY `city_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users_country`
--
ALTER TABLE `users_country`
  MODIFY `country_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users_role`
--
ALTER TABLE `users_role`
  MODIFY `role_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users_state`
--
ALTER TABLE `users_state`
  MODIFY `state_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users_user`
--
ALTER TABLE `users_user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
