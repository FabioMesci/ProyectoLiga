-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 24-07-2023 a las 21:51:36
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyecto_liga`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `admin`
--

CREATE TABLE `admin` (
  `idAdmin` int(11) NOT NULL,
  `user` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `admin`
--

INSERT INTO `admin` (`idAdmin`, `user`, `password`) VALUES
(1, 'admin', '1234');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `calendario_ligas`
--

CREATE TABLE `calendario_ligas` (
  `idCalendario_Ligas` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `fk_idEstadio` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `calendario_ligas`
--

INSERT INTO `calendario_ligas` (`idCalendario_Ligas`, `fecha`, `fk_idEstadio`) VALUES
(1, '2023-07-26', 11),
(4, '2023-07-27', 11),
(5, '2023-07-27', 11),
(6, '2023-07-23', 5),
(7, '2023-07-26', 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `club`
--

CREATE TABLE `club` (
  `nombre_club` varchar(60) NOT NULL,
  `director_tecnico` varchar(45) NOT NULL,
  `año_fundacion` int(11) NOT NULL,
  `presidente_club` varchar(45) NOT NULL,
  `fk_club_tabla_posiciones` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `club`
--

INSERT INTO `club` (`nombre_club`, `director_tecnico`, `año_fundacion`, `presidente_club`, `fk_club_tabla_posiciones`) VALUES
('Club Atlético de Madrid', 'Diego Simeone', 1903, 'Enrique Cerezo', 3),
('FC Barcelona', 'Xavi Hernández', 1899, 'Joan Laporta', 2),
('Manchester City', 'Pep Guardiola', 1880, 'Khaldoon Al Mubarak', 7),
('Real Madrid', 'Carlo Ancelotti', 1802, 'Florentino', 13);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estadio`
--

CREATE TABLE `estadio` (
  `idEstadio` int(11) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `ubicación` text DEFAULT NULL,
  `fk_nombre_club` varchar(60) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estadio`
--

INSERT INTO `estadio` (`idEstadio`, `nombre`, `ubicación`, `fk_nombre_club`) VALUES
(2, 'Camp Nou', 'Por ahi en barcelona', 'FC Barcelona'),
(4, 'Estadio Cívitas Metropolitano', 'Por ahi en Madrid también', 'Club Atlético de Madrid'),
(5, 'Etihad Stadium', 'Por ahi en Manchester', 'Manchester City'),
(11, 'Santiago Bernabeu ', 'Por ahi en Madrid', 'Real Madrid');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estadisticas`
--

CREATE TABLE `estadisticas` (
  `idEstadisticas` int(11) NOT NULL,
  `goleslocales` int(11) NOT NULL DEFAULT 0,
  `golesvisitantes` int(11) NOT NULL DEFAULT 0,
  `porcentaje_posesion_local` int(11) NOT NULL DEFAULT 0,
  `porcentaje_posesion_visitante` int(11) NOT NULL DEFAULT 0,
  `tiros_local` int(11) NOT NULL DEFAULT 0,
  `tiros_visitante` int(11) NOT NULL DEFAULT 0,
  `tirosapuerta_local` int(11) NOT NULL DEFAULT 0,
  `tirosapuerta_visitante` int(11) NOT NULL DEFAULT 0,
  `faltas_local` int(11) NOT NULL DEFAULT 0,
  `faltas_visitante` int(11) NOT NULL DEFAULT 0,
  `tarjetas_amarillas_local` int(11) NOT NULL DEFAULT 0,
  `tarjetas_amarillas_visitante` int(11) NOT NULL DEFAULT 0,
  `offsite_local` int(11) NOT NULL DEFAULT 0,
  `offsite_visitante` int(11) NOT NULL DEFAULT 0,
  `corner_local` int(11) NOT NULL DEFAULT 0,
  `corner_visitante` int(11) NOT NULL DEFAULT 0,
  `fk_Partido_idCalendario_Ligas` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estadisticas`
--

INSERT INTO `estadisticas` (`idEstadisticas`, `goleslocales`, `golesvisitantes`, `porcentaje_posesion_local`, `porcentaje_posesion_visitante`, `tiros_local`, `tiros_visitante`, `tirosapuerta_local`, `tirosapuerta_visitante`, `faltas_local`, `faltas_visitante`, `tarjetas_amarillas_local`, `tarjetas_amarillas_visitante`, `offsite_local`, `offsite_visitante`, `corner_local`, `corner_visitante`, `fk_Partido_idCalendario_Ligas`) VALUES
(2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
(3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4),
(4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5),
(5, 2, 1, 49, 51, 10, 6, 5, 3, 1, 2, 1, 1, 5, 4, 6, 8, 6),
(6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `jugadores`
--

CREATE TABLE `jugadores` (
  `idJugadores` int(11) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `apellido` varchar(45) NOT NULL,
  `edad` int(11) NOT NULL,
  `posicion` varchar(45) NOT NULL,
  `pais_de_origen` varchar(45) NOT NULL,
  `altura_cm` int(11) NOT NULL,
  `fk_nombre_Club` varchar(60) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `jugadores`
--

INSERT INTO `jugadores` (`idJugadores`, `nombre`, `apellido`, `edad`, `posicion`, `pais_de_origen`, `altura_cm`, `fk_nombre_Club`) VALUES
(1, 'Vinicius Jr.', 'Paixao ', 23, 'Delantero', 'Brasil', 176, 'Club Atlético de Madrid');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `partido`
--

CREATE TABLE `partido` (
  `fk_idCalendario_Ligas` int(11) NOT NULL,
  `equipo_local` varchar(45) DEFAULT NULL,
  `equipo_visitante` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `partido`
--

INSERT INTO `partido` (`fk_idCalendario_Ligas`, `equipo_local`, `equipo_visitante`) VALUES
(1, 'FC Barcelona', 'Manchester City'),
(4, 'Real Madrid', 'FC Barcelona'),
(5, 'Club Atlético de Madrid', 'FC Barcelona'),
(6, 'Manchester City', 'Real Madrid'),
(7, 'FC Barcelona', 'Real Madrid');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tabla_posiciones`
--

CREATE TABLE `tabla_posiciones` (
  `idTabla_posiciones` int(11) NOT NULL,
  `partidos_jugados` int(11) NOT NULL,
  `victorias` int(11) NOT NULL,
  `derrotas` int(11) NOT NULL,
  `empates` int(11) NOT NULL,
  `gol_a_favor` int(11) NOT NULL,
  `gol_en_contra` int(11) NOT NULL,
  `puntaje` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tabla_posiciones`
--

INSERT INTO `tabla_posiciones` (`idTabla_posiciones`, `partidos_jugados`, `victorias`, `derrotas`, `empates`, `gol_a_favor`, `gol_en_contra`, `puntaje`) VALUES
(2, 20, 6, 4, 6, 4, 5, 6),
(3, 0, 0, 0, 0, 0, 0, 0),
(7, 0, 0, 0, 0, 0, 0, 0),
(11, 0, 0, 0, 0, 0, 0, 0),
(13, 0, 0, 0, 0, 0, 0, 0);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`idAdmin`),
  ADD UNIQUE KEY `user` (`user`);

--
-- Indices de la tabla `calendario_ligas`
--
ALTER TABLE `calendario_ligas`
  ADD PRIMARY KEY (`idCalendario_Ligas`),
  ADD KEY `fk_idEstadio` (`fk_idEstadio`);

--
-- Indices de la tabla `club`
--
ALTER TABLE `club`
  ADD PRIMARY KEY (`nombre_club`),
  ADD UNIQUE KEY `fk_club_tabla_posiciones` (`fk_club_tabla_posiciones`);

--
-- Indices de la tabla `estadio`
--
ALTER TABLE `estadio`
  ADD PRIMARY KEY (`idEstadio`),
  ADD KEY `fk_nombre_club` (`fk_nombre_club`);

--
-- Indices de la tabla `estadisticas`
--
ALTER TABLE `estadisticas`
  ADD PRIMARY KEY (`idEstadisticas`),
  ADD KEY `fk_Partido_idCalendario_Ligas` (`fk_Partido_idCalendario_Ligas`);

--
-- Indices de la tabla `jugadores`
--
ALTER TABLE `jugadores`
  ADD PRIMARY KEY (`idJugadores`),
  ADD KEY `fk_nombre_Club` (`fk_nombre_Club`);

--
-- Indices de la tabla `partido`
--
ALTER TABLE `partido`
  ADD UNIQUE KEY `fk_idCalendario_Ligas` (`fk_idCalendario_Ligas`),
  ADD KEY `equipo_local` (`equipo_local`),
  ADD KEY `equipo_visitante` (`equipo_visitante`);

--
-- Indices de la tabla `tabla_posiciones`
--
ALTER TABLE `tabla_posiciones`
  ADD PRIMARY KEY (`idTabla_posiciones`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `admin`
--
ALTER TABLE `admin`
  MODIFY `idAdmin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `calendario_ligas`
--
ALTER TABLE `calendario_ligas`
  MODIFY `idCalendario_Ligas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `estadio`
--
ALTER TABLE `estadio`
  MODIFY `idEstadio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `estadisticas`
--
ALTER TABLE `estadisticas`
  MODIFY `idEstadisticas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `jugadores`
--
ALTER TABLE `jugadores`
  MODIFY `idJugadores` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `tabla_posiciones`
--
ALTER TABLE `tabla_posiciones`
  MODIFY `idTabla_posiciones` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `calendario_ligas`
--
ALTER TABLE `calendario_ligas`
  ADD CONSTRAINT `calendario_ligas_ibfk_1` FOREIGN KEY (`fk_idEstadio`) REFERENCES `estadio` (`idEstadio`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `club`
--
ALTER TABLE `club`
  ADD CONSTRAINT `club_ibfk_1` FOREIGN KEY (`fk_club_tabla_posiciones`) REFERENCES `tabla_posiciones` (`idTabla_posiciones`);

--
-- Filtros para la tabla `estadio`
--
ALTER TABLE `estadio`
  ADD CONSTRAINT `estadio_ibfk_1` FOREIGN KEY (`fk_nombre_club`) REFERENCES `club` (`nombre_club`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `estadisticas`
--
ALTER TABLE `estadisticas`
  ADD CONSTRAINT `estadisticas_ibfk_1` FOREIGN KEY (`fk_Partido_idCalendario_Ligas`) REFERENCES `partido` (`fk_idCalendario_Ligas`) ON DELETE CASCADE;

--
-- Filtros para la tabla `jugadores`
--
ALTER TABLE `jugadores`
  ADD CONSTRAINT `jugadores_ibfk_1` FOREIGN KEY (`fk_nombre_Club`) REFERENCES `club` (`nombre_club`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `partido`
--
ALTER TABLE `partido`
  ADD CONSTRAINT `partido_ibfk_1` FOREIGN KEY (`fk_idCalendario_Ligas`) REFERENCES `calendario_ligas` (`idCalendario_Ligas`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `partido_ibfk_2` FOREIGN KEY (`equipo_local`) REFERENCES `club` (`nombre_club`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `partido_ibfk_3` FOREIGN KEY (`equipo_visitante`) REFERENCES `club` (`nombre_club`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
