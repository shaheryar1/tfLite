-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 18, 2020 at 11:08 AM
-- Server version: 10.3.16-MariaDB
-- PHP Version: 7.1.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sai`
--

-- --------------------------------------------------------

--
-- Table structure for table `camera_block`
--

CREATE TABLE `camera_block` (
  `block` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `camera_block`
--

INSERT INTO `camera_block` (`block`) VALUES
(0);

-- --------------------------------------------------------

--
-- Table structure for table `detections`
--

CREATE TABLE `detections` (
  `id` int(3) NOT NULL,
  `entry_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `confidence` float NOT NULL,
  `object_id` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `detections`
--

INSERT INTO `detections` (`id`, `entry_time`, `confidence`, `object_id`) VALUES
(38, '2020-03-12 10:07:08', 70, 43),
(40, '2020-03-12 10:11:40', 70, 43),
(41, '2020-03-12 10:11:56', 70, 43);

-- --------------------------------------------------------

--
-- Table structure for table `objects`
--

CREATE TABLE `objects` (
  `object_id` int(3) NOT NULL,
  `name` varchar(50) NOT NULL,
  `price` float NOT NULL,
  `status` int(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `objects`
--

INSERT INTO `objects` (`object_id`, `name`, `price`, `status`) VALUES
(0, 'person', 0, 1),
(1, 'bicycle', 1.99, 1),
(2, 'car', 3.98, 1),
(3, 'motorcycle', 5.97, 1),
(4, 'airplane', 7.96, 1),
(5, 'bus', 9.95, 1),
(6, 'train', 11.94, 1),
(7, 'truck', 13.93, 1),
(8, 'boat', 15.92, 1),
(9, 'traffic light', 17.91, 1),
(10, 'fire hydrant', 19.9, 1),
(11, '???', 21.89, 1),
(12, 'stop sign', 23.88, 1),
(13, 'parking meter', 25.87, 1),
(14, 'bench', 27.86, 1),
(15, 'bird', 29.85, 1),
(16, 'cat', 31.84, 1),
(17, 'dog', 33.83, 1),
(18, 'horse', 35.82, 1),
(19, 'sheep', 37.81, 1),
(20, 'cow', 39.8, 1),
(21, 'elephant', 41.79, 1),
(22, 'bear', 43.78, 1),
(23, 'zebra', 45.77, 1),
(24, 'giraffe', 47.76, 1),
(25, '???', 49.75, 1),
(26, 'backpack', 51.74, 1),
(27, 'umbrella', 53.73, 1),
(28, '???', 55.72, 1),
(29, '???', 57.71, 1),
(30, 'handbag', 59.7, 1),
(31, 'tie', 61.69, 1),
(32, 'suitcase', 63.68, 1),
(33, 'frisbee', 65.67, 1),
(34, 'skis', 67.66, 1),
(35, 'snowboard', 69.65, 1),
(36, 'sports ball', 71.64, 1),
(37, 'kite', 73.63, 1),
(38, 'baseball bat', 75.62, 1),
(39, 'baseball glove', 77.61, 1),
(40, 'skateboard', 79.6, 1),
(41, 'surfboard', 81.59, 1),
(42, 'tennis racket', 83.58, 1),
(43, 'bottle', 85.57, 1),
(44, '???', 87.56, 1),
(45, 'wine glass', 89.55, 1),
(46, 'cup', 91.54, 1),
(47, 'fork', 93.53, 1),
(48, 'knife', 95.52, 1),
(49, 'spoon', 97.51, 1),
(50, 'bowl', 99.5, 1),
(51, 'banana', 101.49, 1),
(52, 'apple', 103.48, 1),
(53, 'sandwich', 105.47, 1),
(54, 'orange', 107.46, 1),
(55, 'broccoli', 109.45, 1),
(56, 'carrot', 111.44, 1),
(57, 'hot dog', 113.43, 1),
(58, 'pizza', 115.42, 1),
(59, 'donut', 117.41, 1),
(60, 'cake', 119.4, 1),
(61, 'chair', 121.39, 1),
(62, 'couch', 123.38, 1),
(63, 'potted plant', 125.37, 1),
(64, 'bed', 127.36, 1),
(65, '???', 129.35, 1),
(66, 'dining table', 131.34, 1),
(67, '???', 133.33, 1),
(68, '???', 135.32, 1),
(69, 'toilet', 137.31, 1),
(70, '???', 139.3, 1),
(71, 'tv', 141.29, 1),
(72, 'laptop', 143.28, 1),
(73, 'mouse', 145.27, 1),
(74, 'remote', 147.26, 1),
(75, 'keyboard', 149.25, 1),
(76, 'cell phone', 151.24, 1),
(77, 'microwave', 153.23, 1),
(78, 'oven', 155.22, 1),
(79, 'toaster', 157.21, 1),
(80, 'sink', 159.2, 1),
(81, 'refrigerator', 161.19, 1),
(82, '???', 163.18, 1),
(83, 'book', 165.17, 1),
(84, 'clock', 167.16, 1),
(85, 'vase', 169.15, 1),
(86, 'scissors', 171.14, 1),
(87, 'teddy bear', 173.13, 1),
(88, 'hair drier', 175.12, 1),
(89, 'toothbrush', 177.11, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `detections`
--
ALTER TABLE `detections`
  ADD PRIMARY KEY (`id`),
  ADD KEY `object_id` (`object_id`);

--
-- Indexes for table `objects`
--
ALTER TABLE `objects`
  ADD PRIMARY KEY (`object_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `detections`
--
ALTER TABLE `detections`
  MODIFY `id` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `detections`
--
ALTER TABLE `detections`
  ADD CONSTRAINT `detections_ibfk_1` FOREIGN KEY (`object_id`) REFERENCES `objects` (`object_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
