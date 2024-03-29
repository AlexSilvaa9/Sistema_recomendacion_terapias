-- consulta para coger las enfermedades de una persona
Select dni,descripcion
from paciente p,paciente_enfermedad pe,enfermedad e
where p.dni=pe.paciente_dni and pe.enfermedad_codigo_enfermedad=e.codigo_enfermedad and p.dni=95592093;

-- consulta para coger las terapias de una persona 
select p.dni,t.codigo_de_terapia,t.descripcion,t.duracion, pr.fecha_inicio
from paciente p,prescripcion pr, terapia t
where p.dni=pr.paciente_dni and pr.terapia_codigo_de_terapia=t.codigo_de_terapia and p.dni=95592093
order by pr.fecha_inicio desc;

-- consulta para coger las terapias de una persona validadas para que el paciente la pueda ver
select p.dni,t.codigo_de_terapia,t.descripcion,t.duracion
from paciente p,prescripcion pr, terapia t
where p.dni=pr.paciente_dni and pr.terapia_codigo_de_terapia=t.codigo_de_terapia and pr.validacion=1 and p.dni=95592093;

-- query para validar una prescripcion
UPDATE prescripcion pr
SET pr.validacion = 1
WHERE pr.paciente_dni = '95592093'
AND pr.medico_dni = '65112919'
AND pr.terapia_codigo_de_terapia = 'EAGXSAZKBF';

-- Insertar prescripcion (IA)
INSERT INTO prescripcion (fecha_inicio, validacion, paciente_dni, medico_dni, terapia_codigo_de_terapia) VALUES (0, 0, 0, 0, 0);
-- Borrar insertar paciente
INSERT INTO persona (dni, nombre, apellidos, telefono, persona_type) VALUES (0, 0, 0, 0, 0);
INSERT INTO paciente (dni, nss) VALUES (0, 0);

DELETE FROM paciente
WHERE dni=0;