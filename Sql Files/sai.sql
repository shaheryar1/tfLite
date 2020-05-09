-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 10, 2020 at 09:55 AM
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
(16, '2020-03-10 08:40:30', 69, 43);

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
(0, 'person\n', 0, 1),
(1, 'bicycle\n', 1.99, 1),
(2, 'car\n', 3.98, 1),
(3, 'motorcycle\n', 5.97, 1),
(4, 'airplane\n', 7.96, 1),
(5, 'bus\n', 9.95, 1),
(6, 'train\n', 11.94, 1),
(7, 'truck\n', 13.93, 1),
(8, 'boat\n', 15.92, 1),
(9, 'traffic light\n', 17.91, 1),
(10, 'fire hydrant\n', 19.9, 1),
(11, 'stop sign\n', 21.89, 1),
(12, 'parking meter\n', 23.88, 1),
(13, 'bench\n', 25.87, 1),
(14, 'bird\n', 27.86, 1),
(15, 'cat\n', 29.85, 1),
(16, 'dog\n', 31.84, 1),
(17, 'horse\n', 33.83, 1),
(18, 'sheep\n', 35.82, 1),
(19, 'cow\n', 37.81, 1),
(20, 'elephant\n', 39.8, 1),
(21, 'bear\n', 41.79, 1),
(22, 'zebra\n', 43.78, 1),
(23, 'giraffe\n', 45.77, 1),
(24, 'backpack\n', 47.76, 1),
(25, 'umbrella\n', 49.75, 1),
(26, 'handbag\n', 51.74, 1),
(27, 'tie\n', 53.73, 1),
(28, 'suitcase\n', 55.72, 1),
(29, 'frisbee\n', 57.71, 1),
(30, 'skis\n', 59.7, 1),
(31, 'snowboard\n', 61.69, 1),
(32, 'sports ball\n', 63.68, 1),
(33, 'kite\n', 65.67, 1),
(34, 'baseball bat\n', 67.66, 1),
(35, 'baseball glove\n', 69.65, 1),
(36, 'skateboard\n', 71.64, 1),
(37, 'surfboard\n', 73.63, 1),
(38, 'tennis racket\n', 75.62, 1),
(39, 'bottle\n', 77.61, 1),
(40, 'wine glass\n', 79.6, 1),
(41, 'cup\n', 81.59, 1),
(42, 'fork\n', 83.58, 1),
(43, 'knife\n', 85.57, 1),
(44, 'spoon\n', 87.56, 1),
(45, 'bowl\n', 89.55, 1),
(46, 'banana\n', 91.54, 1),
(47, 'apple\n', 93.53, 1),
(48, 'sandwich\n', 95.52, 1),
(49, 'orange\n', 97.51, 1),
(50, 'broccoli\n', 99.5, 1),
(51, 'carrot\n', 101.49, 1),
(52, 'hot dog\n', 103.48, 1),
(53, 'pizza\n', 105.47, 1),
(54, 'donut\n', 107.46, 1),
(55, 'cake\n', 109.45, 1),
(56, 'chair\n', 111.44, 1),
(57, 'couch\n', 113.43, 1),
(58, 'potted plant\n', 115.42, 1),
(59, 'bed\n', 117.41, 1),
(60, 'dining table\n', 119.4, 1),
(61, 'toilet\n', 121.39, 1),
(62, 'tv\n', 123.38, 1),
(63, 'laptop\n', 125.37, 1),
(64, 'mouse\n', 127.36, 1),
(65, 'remote\n', 129.35, 1),
(66, 'keyboard\n', 131.34, 1),
(67, 'cell phone\n', 133.33, 1),
(68, 'microwave\n', 135.32, 1),
(69, 'oven\n', 137.31, 1),
(70, 'toaster\n', 139.3, 1),
(71, 'sink\n', 141.29, 1),
(72, 'refrigerator\n', 143.28, 1),
(73, 'book\n', 145.27, 1),
(74, 'clock\n', 147.26, 1),
(75, 'vase\n', 149.25, 1),
(76, 'scissors\n', 151.24, 1),
(77, 'teddy bear\n', 153.23, 1),
(78, 'hair drier\n', 155.22, 1),
(79, 'toothbrush\n', 157.21, 1);

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
  MODIFY `id` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

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
