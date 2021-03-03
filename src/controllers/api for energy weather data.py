DEVICES
    '''

    def device_object(self, row):
        json.dump({
            'ID': row['ID'],
            'forecast_time': row['forecast_time'],
            'power_output_w': row['power_output_w'],
            'power_output_f0_w': row['power_output_f0_w'],
            'power_output_f10_w': row['power_output_f10_w'],
            'power_output_f25_w': row['power_output_f25_w'],
            'power_output_f50_w': row['power_output_f50_w'],
            'power_output_f75_w': row['power_output_f75_w'],
            'power_output_f90_w': row['power_output_f90_w'],
            'power_output_f100_w': row['power_output_f100_w'],
            'system_temperature_c': row['system_temperature_c']
        }, abc)
        return abc

    def insert_weather_data(self, forecast_time, power_output_w, power_output_f0_w, power_output_f10_w, power_output_f25_w, power_output_f50_w,
                power_output_f75_w, power_output_f90_w, power_output_f100_w, system_temperature_c):
        query = 'INSERT INTO device_info(forecast_time, power_output_w, power_output_f0_w, power_output_f10_w, power_output_f25_w, power_output_f50_w,' \
                'power_output_f75_w, power_output_f90_w, power_output_f100_w, system_temperature_c) VALUES(?,?,?,?,?,?,?,?,?,?)'
        self.foreign_key()
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (device_name, topic, location)
        cur.execute(query, pvalue)
        self.con.commit()
        deviceid = cur.lastrowid
        if cur.rowcount < 1:
            return False
        return deviceid