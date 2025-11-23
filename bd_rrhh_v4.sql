-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 04-11-2025 a las 19:16:10
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bd_rrhh_v4`
--

CREATE DATABASE bd_rrhh_v4;
USE bd_rrhh_v4;

--
-- Estructura de tabla para la tabla `actividadcobro`
--

CREATE TABLE `actividadcobro` (
  `IdActividad` int(11) NOT NULL,
  `IdPedido` int(11) NOT NULL,
  `IdUsuario` int(11) DEFAULT NULL,
  `TipoActividad` enum('Llamada','Correo','Mensaje','Visita') NOT NULL,
  `FechaActividad` datetime NOT NULL DEFAULT current_timestamp(),
  `Comentario` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistencia`
--

CREATE TABLE `asistencia` (
  `IdAsistencia` INT(11) NOT NULL AUTO_INCREMENT,
  `IdUsuario` INT(11) NOT NULL,
  `Fecha` DATE NOT NULL,
  `HoraEntrada` TIME NOT NULL,
  `HoraSalida` TIME DEFAULT NULL,
  `HoraInicioDescanso` TIME DEFAULT NULL,
  `HoraFinDescanso` TIME DEFAULT NULL,
  `Descanso` INT(11) DEFAULT NULL, -- duración en minutos
  `Estado` ENUM('A tiempo', 'Tarde', 'Ausente', 'Descanso','Finalizado') NOT NULL,
  PRIMARY KEY (`IdAsistencia`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `asistencia`
--

INSERT INTO `asistencia` (`IdAsistencia`, `IdUsuario`, `Fecha`, `HoraEntrada`, `HoraSalida`, `Descanso`, `Estado`) VALUES
(4, 18, '2025-11-03', '00:49:00', '12:49:00', 60, ''),
(5, 18, '2025-11-04', '08:01:48', NULL, NULL, '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cartera`
--

CREATE TABLE `cartera` (
  `IdCartera` int(11) NOT NULL,
  `IdUsuario` int(11) NOT NULL,
  `NombreContacto` varchar(100) NOT NULL,
  `TelefonoContacto` varchar(20) NOT NULL,
  `CorreoContacto` varchar(255) NOT NULL,
  `FechaAsignacion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comprobante`
--

CREATE TABLE `comprobante` (
  `IdComprobante` int(11) NOT NULL,
  `IdPedido` int(11) NOT NULL,
  `IdUsuario` int(11) DEFAULT NULL,
  `MontoPagado` decimal(10,2) NOT NULL,
  `FechaPago` datetime NOT NULL DEFAULT current_timestamp(),
  `MetodoPago` enum('Transferencia','Efectivo','Tarjeta') NOT NULL,
  `ArchivoAdjunto` varchar(255) DEFAULT NULL,
  `Verificado` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `denuncia`
--

CREATE TABLE `denuncia` (
  `IdDenuncia` int(11) NOT NULL,
  `IdDenunciante` int(11) DEFAULT NULL,
  `Titulo` varchar(100) NOT NULL,
  `Descripcion` text NOT NULL,
  `Estado` enum('Recibida','En Proceso','Cerrada') NOT NULL,
  `Anonimo` tinyint(1) NOT NULL,
  `Adjunto` varchar(255) DEFAULT NULL,
  `FechaCreacion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `documento`
--

CREATE TABLE `documento` (
  `IdDocumento` int(11) NOT NULL,
  `IdUsuario` int(11) NOT NULL,
  `NombreArchivo` varchar(255) NOT NULL,
  `TipoArchivo` varchar(50) DEFAULT NULL,
  `RutaArchivo` varchar(255) NOT NULL,
  `FechaSubida` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `encuesta`
--

CREATE TABLE `encuesta` (
  `IdEncuesta` int(11) NOT NULL,
  `NombreEncuesta` varchar(255) NOT NULL,
  `Descripcion` text NOT NULL,
  `FechaCreacion` date NOT NULL,
  `Estado` enum('Activa','Inactiva') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historialpedido`
--

CREATE TABLE `historialpedido` (
  `IdHistorial` int(11) NOT NULL,
  `IdPedido` int(11) NOT NULL,
  `IdUsuario` int(11) NOT NULL,
  `EstadoAnterior` varchar(50) DEFAULT NULL,
  `EstadoNuevo` varchar(50) DEFAULT NULL,
  `FechaCambio` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horario`
--

CREATE TABLE `horario` (
  `IdHorario` int(11) NOT NULL,
  `IdUsuario` int(11) NOT NULL,
  `FechaInicio` date NOT NULL,
  `FechaFin` date NOT NULL,
  `HoraEntradaP` time NOT NULL,
  `HoraSalidaP` time NOT NULL,
  `DescansoP` int(11) NOT NULL,
  `TipoJornada` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `noticia`
--

CREATE TABLE `noticia` (
  `IdNoticia` int(11) NOT NULL,
  `IdUsuario` int(11) NOT NULL,
  `Titulo` varchar(200) NOT NULL,
  `Contenido` text NOT NULL,
  `FechaPublicacion` datetime NOT NULL DEFAULT current_timestamp(),
  `Estado` varchar(50) NOT NULL DEFAULT 'Borrador',
  `FechaModificacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedido`
--

CREATE TABLE `pedido` (
  `IdPedido` int(11) NOT NULL,
  `IdCartera` int(11) NOT NULL,
  `NumeroPedido` varchar(50) NOT NULL,
  `FechaCreacion` date NOT NULL,
  `FechaVencimiento` date NOT NULL,
  `ValorPedido` decimal(10,2) NOT NULL,
  `MontoPagado` decimal(10,2) NOT NULL DEFAULT 0.00,
  `MontoPendiente` decimal(10,2) NOT NULL DEFAULT 0.00,
  `DocumentoAdjunto` varchar(255) DEFAULT NULL,
  `Estado` enum('Pendiente','En Gestión','Pago Parcial','Cancelado','Cobrado') NOT NULL DEFAULT 'Pendiente'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preguntas`
--

CREATE TABLE `preguntas` (
  `IdPregunta` int(11) NOT NULL,
  `IdEncuesta` int(11) NOT NULL,
  `TextoPregunta` text NOT NULL,
  `TipoPregunta` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `programacion`
--

CREATE TABLE `programacion` (
  `IdProgramacion` int(11) NOT NULL,
  `IdUsuario` int(11) NOT NULL,
  `IdEncuesta` int(11) NOT NULL,
  `FechaAsignacion` date NOT NULL,
  `FechaLimite` date DEFAULT NULL,
  `Estado` enum('Pendiente','Completada','Vencida') NOT NULL,
  `FechaCompletado` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reconocimiento`
--

CREATE TABLE `reconocimiento` (
  `IdReconocimiento` int(11) NOT NULL,
  `IdUsuario` int(11) NOT NULL,
  `TipoReconocimiento` varchar(50) NOT NULL,
  `Motivo` text NOT NULL,
  `FechaOtorgado` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `respuesta`
--

CREATE TABLE `respuesta` (
  `IdRespuesta` int(11) NOT NULL,
  `IdPregunta` int(11) NOT NULL,
  `IdUsuario` int(11) NOT NULL,
  `TextoRespuesta` text DEFAULT NULL,
  `OpcionSeleccionada` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE `rol` (
  `IdRol` int(11) NOT NULL,
  `NombreRol` varchar(50) NOT NULL,
  `Descripcion` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `rol`
--

INSERT INTO `rol` (`IdRol`, `NombreRol`, `Descripcion`) VALUES
(9, 'Administrador', 'Admin'),
(11, 'Vendedora', ''),
(12, 'Contadora', ''),
(13, 'Bodega', ''),
(14, 'Dentista', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `solicitud`
--

CREATE TABLE `solicitud` (
  `IdSolicitud` int(11) NOT NULL,
  `IdUsuario` int(11) NOT NULL,
  `IdTipoSolicitud` int(11) NOT NULL,
  `FechaSolicitud` date NOT NULL,
  `FechaInicio` date NOT NULL,
  `HoraInicio` time DEFAULT NULL,
  `FechaFin` date NOT NULL,
  `HoraFin` time DEFAULT NULL,
  `DiasSolicitados` int(11) NOT NULL,
  `FechaAprobado` date DEFAULT NULL,
  `Justificacion` text NOT NULL,
  `DocumentoAd` varchar(255) DEFAULT NULL,
  `Estado` enum('Pendiente','Aprobada','Rechazada') NOT NULL,
  `Observaciones` text DEFAULT NULL,
  `RutaAdjunto` varchar(255) DEFAULT NULL,
  `Tipo` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `solicitud`
--

INSERT INTO `solicitud` (`IdSolicitud`, `IdUsuario`, `IdTipoSolicitud`, `FechaSolicitud`, `FechaInicio`, `HoraInicio`, `FechaFin`, `HoraFin`, `DiasSolicitados`, `FechaAprobado`, `Justificacion`, `DocumentoAd`, `Estado`, `Observaciones`, `RutaAdjunto`, `Tipo`) VALUES
(5, 18, 1, '2025-11-04', '2025-11-01', '06:55:00', '2025-11-08', '18:55:00', 8, NULL, 'Vacaciones ', NULL, 'Aprobada', NULL, NULL, NULL),
(6, 18, 2, '2025-11-04', '2025-11-01', '07:12:00', '2025-11-04', '19:12:00', 4, NULL, 'Si', NULL, 'Aprobada', NULL, NULL, NULL),
(7, 18, 2, '2025-11-04', '2025-11-03', '07:25:00', '2025-11-19', '19:25:00', 17, NULL, 'Sisi', NULL, 'Rechazada', NULL, NULL, NULL),
(8, 18, 3, '2025-11-04', '2025-11-18', '07:30:00', '2025-11-20', '19:30:00', 3, NULL, 'sisisi', NULL, 'Aprobada', NULL, NULL, NULL),
(9, 18, 5, '2025-11-04', '2025-11-06', '07:42:00', '2025-11-12', '19:42:00', 7, NULL, 'SISISI', NULL, 'Aprobada', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tiposolicitud`
--

CREATE TABLE `tiposolicitud` (
  `IdTipoSolicitud` int(11) NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tiposolicitud`
--

INSERT INTO `tiposolicitud` (`IdTipoSolicitud`, `Nombre`, `Descripcion`) VALUES
(1, 'Vacaciones', 'Solicitud de días de descanso programados según política de vacaciones.'),
(2, 'Permiso Personal', 'Solicitud de ausencia por motivos personales o familiares.'),
(3, 'Permiso Médico', 'Solicitud de permiso para citas médicas o reposo por incapacidad.'),
(4, 'Capacitación', 'Solicitud de permiso para asistir a capacitaciones o cursos externos.'),
(5, 'Maternidad/Paternidad', 'Solicitud de permiso por nacimiento o adopción de un hijo.'),
(6, 'Luto', 'Solicitud de permiso por fallecimiento de un familiar cercano.'),
(7, 'Estudio', 'Solicitud de permiso para presentar exámenes o asistir a clases.'),
(8, 'Otro', 'Solicitud de permiso por otra razón no contemplada en las categorías anteriores.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `IdUsuario` int(11) NOT NULL,
  `IdRol` int(11) NOT NULL,
  `Nombres` varchar(100) NOT NULL,
  `Apellidos` varchar(100) NOT NULL,
  `TipoDocumento` varchar(50) NOT NULL,
  `Documento` varchar(50) NOT NULL,
  `Correo` varchar(255) NOT NULL,
  `CorreoCorporativo` varchar(255) NOT NULL,
  `FechaContratacion` date NOT NULL,
  `FechaNacimiento` date NOT NULL,
  `Telefono` varchar(20) NOT NULL,
  `Contrasena` varchar(255) NOT NULL,
  `Estado` tinyint(1) NOT NULL,
  `ResetToken` varchar(100) DEFAULT NULL,
  `ResetExpiracion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`IdUsuario`, `IdRol`, `Nombres`, `Apellidos`, `TipoDocumento`, `Documento`, `Correo`, `CorreoCorporativo`, `FechaContratacion`, `FechaNacimiento`, `Telefono`, `Contrasena`, `Estado`, `ResetToken`, `ResetExpiracion`) VALUES
(17, 9, 'Sergio', 'Llanos', 'CC', '1028863332', 'sllanosceballos@gmail.com', 'llanos@empresa.com', '2025-09-02', '2025-09-01', '3012346089', 'scrypt:32768:8:1$yIiK4NDG2iAVnd8F$3ae15ae0d0f14a15b83fabea543673fef8dff512c409d8155b1266ed03ccb5f7700a39216ee903250c0136b1fa03edbfd01553e0bde0cd710d11b6081e850f1d', 1, '2a3d8ade-895d-490c-a827-4ce0431c7436', '2025-11-04 11:36:38'),
(18, 11, 'Daniel', 'Ovalle', 'CC', '1028865552', 's.ll4nzz@gmail.com', 'ovalle1@empresa.com', '2025-09-26', '2025-09-26', '3002965874', 'scrypt:32768:8:1$8NURiYLax33AHvx3$ba8bb731166753ca988bb074535aae99b3ad75025cd4015d7d015e8b9d5cf983cb6af6c44dc9fb2e97f187bdcdf2b7d8504d8a09ca86f5939222ad9526e8cb73', 1, '48367b32-d5a7-4e23-ba42-9f40d9ab1d95', '2025-11-04 11:37:58'),
(19, 12, 'Nicolas', 'Londoño', 'CC', '1028863333', 'nico@gmail.com', 'nico1@empresa.com', '2025-11-03', '2025-11-02', '3013284975', 'scrypt:32768:8:1$0YJZZxDMYX15p8uw$41cd9ed488bed2b2e9b031e884d2e464527954efc0c64fed32b4002f699d7b35fd255ea36d29eb62ae07e8e3406b870b2659252cfda0951513d22657705c2355', 1, NULL, NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `actividadcobro`
--
ALTER TABLE `actividadcobro`
  ADD PRIMARY KEY (`IdActividad`),
  ADD KEY `IdPedido` (`IdPedido`),
  ADD KEY `IdUsuario` (`IdUsuario`);

--
-- Indices de la tabla `asistencia`
--
ALTER TABLE `asistencia`
  ADD KEY `IdUsuario` (`IdUsuario`);

--
-- Indices de la tabla `cartera`
--
ALTER TABLE `cartera`
  ADD PRIMARY KEY (`IdCartera`),
  ADD KEY `IdUsuario` (`IdUsuario`);

--
-- Indices de la tabla `comprobante`
--
ALTER TABLE `comprobante`
  ADD PRIMARY KEY (`IdComprobante`),
  ADD KEY `IdPedido` (`IdPedido`),
  ADD KEY `IdUsuario` (`IdUsuario`);

--
-- Indices de la tabla `denuncia`
--
ALTER TABLE `denuncia`
  ADD PRIMARY KEY (`IdDenuncia`),
  ADD KEY `IdDenunciante` (`IdDenunciante`);

--
-- Indices de la tabla `documento`
--
ALTER TABLE `documento`
  ADD PRIMARY KEY (`IdDocumento`),
  ADD KEY `IdUsuario` (`IdUsuario`);

--
-- Indices de la tabla `encuesta`
--
ALTER TABLE `encuesta`
  ADD PRIMARY KEY (`IdEncuesta`);

--
-- Indices de la tabla `historialpedido`
--
ALTER TABLE `historialpedido`
  ADD PRIMARY KEY (`IdHistorial`),
  ADD KEY `IdPedido` (`IdPedido`),
  ADD KEY `IdUsuario` (`IdUsuario`);

--
-- Indices de la tabla `horario`
--
ALTER TABLE `horario`
  ADD PRIMARY KEY (`IdHorario`),
  ADD KEY `IdUsuario` (`IdUsuario`);

--
-- Indices de la tabla `noticia`
--
ALTER TABLE `noticia`
  ADD PRIMARY KEY (`IdNoticia`),
  ADD KEY `IdUsuario` (`IdUsuario`);

--
-- Indices de la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD PRIMARY KEY (`IdPedido`),
  ADD KEY `IdCartera` (`IdCartera`);

--
-- Indices de la tabla `preguntas`
--
ALTER TABLE `preguntas`
  ADD PRIMARY KEY (`IdPregunta`),
  ADD KEY `IdEncuesta` (`IdEncuesta`);

--
-- Indices de la tabla `programacion`
--
ALTER TABLE `programacion`
  ADD PRIMARY KEY (`IdProgramacion`),
  ADD KEY `IdUsuario` (`IdUsuario`),
  ADD KEY `IdEncuesta` (`IdEncuesta`);

--
-- Indices de la tabla `reconocimiento`
--
ALTER TABLE `reconocimiento`
  ADD PRIMARY KEY (`IdReconocimiento`),
  ADD KEY `IdUsuario` (`IdUsuario`);

--
-- Indices de la tabla `respuesta`
--
ALTER TABLE `respuesta`
  ADD PRIMARY KEY (`IdRespuesta`),
  ADD KEY `IdPregunta` (`IdPregunta`),
  ADD KEY `IdUsuario` (`IdUsuario`);

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`IdRol`);

--
-- Indices de la tabla `solicitud`
--
ALTER TABLE `solicitud`
  ADD PRIMARY KEY (`IdSolicitud`),
  ADD KEY `IdUsuario` (`IdUsuario`),
  ADD KEY `IdTipoSolicitud` (`IdTipoSolicitud`);

--
-- Indices de la tabla `tiposolicitud`
--
ALTER TABLE `tiposolicitud`
  ADD PRIMARY KEY (`IdTipoSolicitud`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`IdUsuario`),
  ADD UNIQUE KEY `Documento` (`Documento`),
  ADD UNIQUE KEY `Correo` (`Correo`),
  ADD UNIQUE KEY `CorreoCorporativo` (`CorreoCorporativo`),
  ADD KEY `IdRol` (`IdRol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `actividadcobro`
--
ALTER TABLE `actividadcobro`
  MODIFY `IdActividad` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `asistencia`
--
ALTER TABLE `asistencia`
  MODIFY `IdAsistencia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `cartera`
--
ALTER TABLE `cartera`
  MODIFY `IdCartera` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `comprobante`
--
ALTER TABLE `comprobante`
  MODIFY `IdComprobante` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `denuncia`
--
ALTER TABLE `denuncia`
  MODIFY `IdDenuncia` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `documento`
--
ALTER TABLE `documento`
  MODIFY `IdDocumento` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `encuesta`
--
ALTER TABLE `encuesta`
  MODIFY `IdEncuesta` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `historialpedido`
--
ALTER TABLE `historialpedido`
  MODIFY `IdHistorial` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `horario`
--
ALTER TABLE `horario`
  MODIFY `IdHorario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `noticia`
--
ALTER TABLE `noticia`
  MODIFY `IdNoticia` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pedido`
--
ALTER TABLE `pedido`
  MODIFY `IdPedido` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `preguntas`
--
ALTER TABLE `preguntas`
  MODIFY `IdPregunta` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `programacion`
--
ALTER TABLE `programacion`
  MODIFY `IdProgramacion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `reconocimiento`
--
ALTER TABLE `reconocimiento`
  MODIFY `IdReconocimiento` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `respuesta`
--
ALTER TABLE `respuesta`
  MODIFY `IdRespuesta` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `IdRol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `solicitud`
--
ALTER TABLE `solicitud`
  MODIFY `IdSolicitud` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `tiposolicitud`
--
ALTER TABLE `tiposolicitud`
  MODIFY `IdTipoSolicitud` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `IdUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `actividadcobro`
--
ALTER TABLE `actividadcobro`
ADD CONSTRAINT `actividadcobro_ibfk_1` FOREIGN KEY (`IdPedido`) REFERENCES `pedido` (`IdPedido`)
ON DELETE CASCADE;

ALTER TABLE `actividadcobro`
ADD CONSTRAINT `actividadcobro_ibfk_2` FOREIGN KEY (`IdUsuario`) REFERENCES `usuario` (`IdUsuario`);
  
ALTER TABLE actividadcobro
DROP FOREIGN KEY actividadcobro_ibfk_1;

ALTER TABLE actividadcobro
ADD CONSTRAINT actividadcobro_ibfk_1
    FOREIGN KEY (IdPedido)
    REFERENCES pedido(IdPedido)
    ON DELETE CASCADE;


--
-- Filtros para la tabla `asistencia`
--
ALTER TABLE `asistencia`
  ADD CONSTRAINT `asistencia_ibfk_1` FOREIGN KEY (`IdUsuario`) REFERENCES `usuario` (`IdUsuario`);

--
-- Filtros para la tabla `cartera`
--
ALTER TABLE `cartera`
  ADD CONSTRAINT `cartera_ibfk_1` FOREIGN KEY (`IdUsuario`) REFERENCES `usuario` (`IdUsuario`);

--
-- Filtros para la tabla `comprobante`
--
ALTER TABLE `comprobante`
  ADD CONSTRAINT `comprobante_ibfk_1` FOREIGN KEY (`IdPedido`) REFERENCES `pedido` (`IdPedido`) ON DELETE CASCADE,
  ADD CONSTRAINT `comprobante_ibfk_2` FOREIGN KEY (`IdUsuario`) REFERENCES `usuario` (`IdUsuario`) ON DELETE SET NULL;

--
-- Filtros para la tabla `denuncia`
--
ALTER TABLE `denuncia`
  ADD CONSTRAINT `denuncia_ibfk_1` FOREIGN KEY (`IdDenunciante`) REFERENCES `usuario` (`IdUsuario`);

--
-- Filtros para la tabla `documento`
--
ALTER TABLE `documento`
  ADD CONSTRAINT `documento_ibfk_1` FOREIGN KEY (`IdUsuario`) REFERENCES `usuario` (`IdUsuario`);

--
-- Filtros para la tabla `historialpedido`
--
ALTER TABLE `historialpedido`
  ADD CONSTRAINT `historialpedido_ibfk_1` FOREIGN KEY (`IdPedido`) REFERENCES `pedido` (`IdPedido`),
  ADD CONSTRAINT `historialpedido_ibfk_2` FOREIGN KEY (`IdUsuario`) REFERENCES `usuario` (`IdUsuario`);

--
-- Filtros para la tabla `horario`
--
ALTER TABLE `horario`
  ADD CONSTRAINT `horario_ibfk_1` FOREIGN KEY (`IdUsuario`) REFERENCES `usuario` (`IdUsuario`);

--
-- Filtros para la tabla `noticia`
--
ALTER TABLE `noticia`
  ADD CONSTRAINT `noticia_ibfk_1` FOREIGN KEY (`IdUsuario`) REFERENCES `usuario` (`IdUsuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`IdCartera`) REFERENCES `cartera` (`IdCartera`);

--
-- Filtros para la tabla `preguntas`
--
ALTER TABLE `preguntas`
  ADD CONSTRAINT `preguntas_ibfk_1` FOREIGN KEY (`IdEncuesta`) REFERENCES `encuesta` (`IdEncuesta`);

--
-- Filtros para la tabla `programacion`
--
ALTER TABLE `programacion`
  ADD CONSTRAINT `programacion_ibfk_1` FOREIGN KEY (`IdUsuario`) REFERENCES `usuario` (`IdUsuario`),
  ADD CONSTRAINT `programacion_ibfk_2` FOREIGN KEY (`IdEncuesta`) REFERENCES `encuesta` (`IdEncuesta`);

--
-- Filtros para la tabla `reconocimiento`
--
ALTER TABLE `reconocimiento`
  ADD CONSTRAINT `reconocimiento_ibfk_1` FOREIGN KEY (`IdUsuario`) REFERENCES `usuario` (`IdUsuario`);

--
-- Filtros para la tabla `respuesta`
--
ALTER TABLE `respuesta`
  ADD CONSTRAINT `respuesta_ibfk_1` FOREIGN KEY (`IdPregunta`) REFERENCES `preguntas` (`IdPregunta`),
  ADD CONSTRAINT `respuesta_ibfk_2` FOREIGN KEY (`IdUsuario`) REFERENCES `usuario` (`IdUsuario`);

--
-- Filtros para la tabla `solicitud`
--
ALTER TABLE `solicitud`
  ADD CONSTRAINT `solicitud_ibfk_1` FOREIGN KEY (`IdUsuario`) REFERENCES `usuario` (`IdUsuario`),
  ADD CONSTRAINT `solicitud_ibfk_2` FOREIGN KEY (`IdTipoSolicitud`) REFERENCES `tiposolicitud` (`IdTipoSolicitud`);

--
-- Filtros para la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`IdRol`) REFERENCES `rol` (`IdRol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;