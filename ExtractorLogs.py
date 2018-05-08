import luigi

#En la clase solo vamos a cargar un archivo externo, en nuestro caso es el archivo generado por los logs
# Es por eso que solo se requiere la funcion output()
class readLogFile(luigi.ExternalTask):

    def output(self):
        #En esta sentencia est
        return luigi.LocalTarget('archivos/accesos.log')

#Clase en la cual tomaremos las ips del archivo file.log
class grabIPs(luigi.Task):  # Clase estandar de luigi

    def requires(self):
        # Vamos a leer el archivo que se procesara
        return readLogFile()

    def run(self):
        ips = [] #almacenaremos las ip del archivo de logs

        # use the file passed from the previous task
        with self.input().open() as f:
            for line in f:
                # la primera linea se encuentran las ip
                ip = line.split()[0]
                ips.append(ip) #agregamos la ip
            # contamos el numero de ips
            num_ips = len(ips)
        # escribimos las ips
        with self.output().open('w') as f:
            for i in ips:
                f.write(i+"\n")
            f.write("Total de ips:"+str(num_ips))

    def output(self):
        # los resultados son almacenados en el siguiente archivo: numips.txt
        return luigi.LocalTarget('archivos/numips.txt')


if __name__ == '__main__':
    luigi.run(["--local-scheduler"], main_task_cls=grabIPs)#Le decimos que la tarea contigua a ser ejecutada es la clase grabIPs