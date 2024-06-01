-- Generado por Oracle SQL Developer Data Modeler 22.2.0.165.1149
--   en:        2024-03-28 15:51:17 CET
--   sitio:      Oracle Database 11g
--   tipo:      Oracle Database 11g



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE enfermedad (
    codigo_enfermedad VARCHAR2(30 CHAR) NOT NULL,
    descripcion       VARCHAR2(60 CHAR)
);

ALTER TABLE enfermedad ADD CONSTRAINT enfermedad_pk PRIMARY KEY ( codigo_enfermedad );

CREATE TABLE medico (
    dni          VARCHAR2(9 CHAR) NOT NULL,
    especialidad VARCHAR2(40 CHAR)
);

ALTER TABLE medico ADD CONSTRAINT medico_pk PRIMARY KEY ( dni );

CREATE TABLE paciente (
    dni VARCHAR2(9 CHAR) NOT NULL,
    nss VARCHAR2(30 CHAR) NOT NULL
);

ALTER TABLE paciente ADD CONSTRAINT paciente_pk PRIMARY KEY ( dni );

CREATE TABLE paciente_enfermedad (
    paciente_dni                 VARCHAR2(9 CHAR) NOT NULL,
    enfermedad_codigo_enfermedad VARCHAR2(30 CHAR) NOT NULL
);

ALTER TABLE paciente_enfermedad ADD CONSTRAINT relation_6_pk PRIMARY KEY ( paciente_dni,
                                                                           enfermedad_codigo_enfermedad );

CREATE TABLE persona (
    dni          VARCHAR2(9 CHAR) NOT NULL,
    nombre       VARCHAR2(30 CHAR) NOT NULL,
    apellidos    VARCHAR2(30 CHAR) NOT NULL,
    telefono     NUMBER NOT NULL,
    persona_type VARCHAR2(8) NOT NULL
);

ALTER TABLE persona
    ADD CONSTRAINT ch_inh_persona CHECK ( persona_type IN ( 'Medico', 'Paciente', 'Persona' ) );

ALTER TABLE persona ADD CONSTRAINT persona_pk PRIMARY KEY ( dni );

CREATE TABLE prescripcion (
    fecha_inicio              DATE NOT NULL,
    validacion                CHAR(1),
    paciente_dni              VARCHAR2(9 CHAR) NOT NULL,
    medico_dni                VARCHAR2(9 CHAR) NOT NULL,
    terapia_codigo_de_terapia VARCHAR2(30) NOT NULL
);

ALTER TABLE prescripcion
    ADD CONSTRAINT prescripcion_pk PRIMARY KEY ( fecha_inicio,
                                                 paciente_dni,
                                                 terapia_codigo_de_terapia,
                                                 medico_dni );

CREATE TABLE terapia (
    codigo_de_terapia VARCHAR2(30) NOT NULL,
    descripcion       VARCHAR2(100 CHAR),
    duracion          DATE
);

ALTER TABLE terapia ADD CONSTRAINT terapia_pk PRIMARY KEY ( codigo_de_terapia );

ALTER TABLE medico
    ADD CONSTRAINT medico_persona_fk FOREIGN KEY ( dni )
        REFERENCES persona ( dni );

ALTER TABLE paciente
    ADD CONSTRAINT paciente_persona_fk FOREIGN KEY ( dni )
        REFERENCES persona ( dni );

ALTER TABLE prescripcion
    ADD CONSTRAINT prescripcion_medico_fk FOREIGN KEY ( medico_dni )
        REFERENCES medico ( dni );

ALTER TABLE prescripcion
    ADD CONSTRAINT prescripcion_paciente_fk FOREIGN KEY ( paciente_dni )
        REFERENCES paciente ( dni );

ALTER TABLE prescripcion
    ADD CONSTRAINT prescripcion_terapia_fk FOREIGN KEY ( terapia_codigo_de_terapia )
        REFERENCES terapia ( codigo_de_terapia );

ALTER TABLE paciente_enfermedad
    ADD CONSTRAINT relation_6_enfermedad_fk FOREIGN KEY ( enfermedad_codigo_enfermedad )
        REFERENCES enfermedad ( codigo_enfermedad );

ALTER TABLE paciente_enfermedad
    ADD CONSTRAINT relation_6_paciente_fk FOREIGN KEY ( paciente_dni )
        REFERENCES paciente ( dni );

CREATE OR REPLACE TRIGGER arc_fkarc_1_paciente BEFORE
    INSERT OR UPDATE OF dni ON paciente
    FOR EACH ROW
DECLARE
    d VARCHAR2(8);
BEGIN
    SELECT
        a.persona_type
    INTO d
    FROM
        persona a
    WHERE
        a.dni = :new.dni;

    IF ( d IS NULL OR d <> 'Paciente' ) THEN
        raise_application_error(-20223, 'FK Paciente_Persona_FK in Table Paciente violates Arc constraint on Table Persona - discriminator column Persona_TYPE doesn''t have value ''Paciente'''
        );
    END IF;

EXCEPTION
    WHEN no_data_found THEN
        NULL;
    WHEN OTHERS THEN
        RAISE;
END;
/

CREATE OR REPLACE TRIGGER arc_fkarc_1_medico BEFORE
    INSERT OR UPDATE OF dni ON medico
    FOR EACH ROW
DECLARE
    d VARCHAR2(8);
BEGIN
    SELECT
        a.persona_type
    INTO d
    FROM
        persona a
    WHERE
        a.dni = :new.dni;

    IF ( d IS NULL OR d <> 'Medico' ) THEN
        raise_application_error(-20223, 'FK Medico_Persona_FK in Table Medico violates Arc constraint on Table Persona - discriminator column Persona_TYPE doesn''t have value ''Medico'''
        );
    END IF;

EXCEPTION
    WHEN no_data_found THEN
        NULL;
    WHEN OTHERS THEN
        RAISE;
END;
/



-- Informe de Resumen de Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                             7
-- CREATE INDEX                             0
-- ALTER TABLE                             15
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           2
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
