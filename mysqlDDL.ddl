USE Recomendacion_terapias;

CREATE TABLE enfermedad (
    codigo_enfermedad VARCHAR(30) NOT NULL,
    descripcion       VARCHAR(60),
    PRIMARY KEY (codigo_enfermedad)
);

CREATE TABLE medico (
    dni          VARCHAR(9) NOT NULL,
    especialidad VARCHAR(40),
    PRIMARY KEY (dni)
);

CREATE TABLE paciente (
    dni VARCHAR(9) NOT NULL,
    nss VARCHAR(30) NOT NULL,
    PRIMARY KEY (dni)
);

CREATE TABLE paciente_enfermedad (
    paciente_dni                 VARCHAR(9) NOT NULL,
    enfermedad_codigo_enfermedad VARCHAR(30) NOT NULL,
    PRIMARY KEY (paciente_dni, enfermedad_codigo_enfermedad),
    FOREIGN KEY (paciente_dni) REFERENCES paciente (dni),
    FOREIGN KEY (enfermedad_codigo_enfermedad) REFERENCES enfermedad (codigo_enfermedad)
);

CREATE TABLE persona (
    dni          VARCHAR(9) NOT NULL,
    nombre       VARCHAR(30) NOT NULL,
    apellidos    VARCHAR(30) NOT NULL,
    telefono     INT NOT NULL,
    persona_type ENUM('Medico', 'Paciente', 'Persona') NOT NULL,
    PRIMARY KEY (dni)
);

CREATE TABLE prescripcion (
    fecha_inicio              DATE NOT NULL,
    validacion                CHAR(1),
    paciente_dni              VARCHAR(9) NOT NULL,
    medico_dni                VARCHAR(9) NOT NULL,
    terapia_codigo_de_terapia VARCHAR(30) NOT NULL,
    PRIMARY KEY (fecha_inicio, paciente_dni, terapia_codigo_de_terapia, medico_dni),
    FOREIGN KEY (paciente_dni) REFERENCES paciente (dni),
    FOREIGN KEY (medico_dni) REFERENCES medico (dni),
    FOREIGN KEY (terapia_codigo_de_terapia) REFERENCES terapia (codigo_de_terapia)
);

CREATE TABLE terapia (
    codigo_de_terapia VARCHAR(30) NOT NULL,
    descripcion       VARCHAR(100),
    duracion          DATE,
    PRIMARY KEY (codigo_de_terapia)
);

DELIMITER $$

CREATE TRIGGER arc_fkarc_1_paciente BEFORE INSERT ON paciente
FOR EACH ROW
BEGIN
    DECLARE d VARCHAR(8);
    SELECT persona_type INTO d FROM persona WHERE dni = NEW.dni;
    IF d IS NULL OR d <> 'Paciente' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FK Paciente_Persona_FK in Table Paciente violates Arc constraint on Table Persona - discriminator column Persona_TYPE doesn''t have value ''Paciente''';
    END IF;
END$$



CREATE TRIGGER arc_fkarc_1_medico BEFORE INSERT ON medico
FOR EACH ROW
BEGIN
    DECLARE d VARCHAR(8);
    SELECT persona_type INTO d FROM persona WHERE dni = NEW.dni;
    IF d IS NULL OR d <> 'Medico' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FK Medico_Persona_FK in Table Medico violates Arc constraint on Table Persona - discriminator column Persona_TYPE doesn''t have value ''Medico''';
    END IF;
END$$

DELIMITER ;
