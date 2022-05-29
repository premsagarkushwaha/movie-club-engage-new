-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.2:3307
-- Generation Time: May 26, 2022 at 12:30 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `newdata`
--

-- --------------------------------------------------------

--
-- Table structure for table `likedmovie`
--

CREATE TABLE `likedmovie` (
  `id` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `moviename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `likedmovie`
--

INSERT INTO `likedmovie` (`id`, `email`, `moviename`) VALUES
(1, 'prem@gmail.com', 'deadpool'),
(2, 'harsh@gmail.com', 'avatar'),
(3, 'harsh@gmail.com', 'the matrix');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `uname` varchar(25) NOT NULL,
  `umail` varchar(25) NOT NULL,
  `uphone` varchar(14) NOT NULL,
  `upass` varchar(30) NOT NULL,
  `cupass` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `uname`, `umail`, `uphone`, `upass`, `cupass`) VALUES
(1, 'prem', 'prem@gmail.com', '9164783523', '1234', '1234'),
(2, 'thor', 'harsh@gmail.com', '9164783528', '1234', '1234');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `likedmovie`
--
ALTER TABLE `likedmovie`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`,`umail`),
  ADD UNIQUE KEY `unique` (`uphone`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `likedmovie`
--
ALTER TABLE `likedmovie`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
