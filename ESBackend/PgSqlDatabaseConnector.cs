using System;
using System.Collections.Generic;
using ESBackend.DataContract;
using Npgsql;

namespace ESBackend
{
    public class PgSqlDatabaseConnector : IDatabaseConnector
    {
        private static readonly string connString = "Host=es.giorgos.io;Username=esuser;Password=ok0dikosmou123;Database=esdb";

        public PgSqlDatabaseConnector()
        {

        }

        public void InsertDeviceData(double angle, double accel, DateTime timestamp) 
        {
            using (var conn = new NpgsqlConnection(connString))
            {
                conn.Open();

                using(var cmd = new NpgsqlCommand()) 
                {
                    cmd.Connection = conn;
                    cmd.CommandText = "INSERT INTO devicedata (angle, deviceId, timestamp, accelStd) VALUES (@a, @d, @t, @s)";
                    cmd.Parameters.AddWithValue("a", angle);
                    cmd.Parameters.AddWithValue("d", 1);
                    cmd.Parameters.AddWithValue("t", timestamp);
                    cmd.Parameters.AddWithValue("s", accel);
                 try {
                    cmd.ExecuteNonQuery();
                 }
                 catch(Exception ex) 
                 {
                     Console.WriteLine(ex);
                 }
                }
            }

        }

        public IEnumerable<DeviceData> SelectDeviceData(DateTime from, DateTime to)
        {
            using (var conn = new NpgsqlConnection(connString))
            {
                conn.Open();

                using(var cmd = new NpgsqlCommand()) 
                {
                    List<DeviceData> data = new List<DeviceData>();
                    cmd.Connection = conn;
                    cmd.CommandText = "SELECT timestamp, angle, accelstd FROM devicedata WHERE timestamp BETWEEN @f AND @t";
                    cmd.Parameters.AddWithValue("f", from);
                    cmd.Parameters.AddWithValue("t", to);
                    try 
                    {
                        using(var reader = cmd.ExecuteReader())
                        {
                            while(reader.Read()) 
                            {
                                data.Add(new DeviceData(reader.GetDateTime(0), reader.GetDouble(1), reader.GetDouble(2)));
                            }
                        }
                    }
                    catch(Exception ex) 
                    {
                        Console.WriteLine(ex);
                    }
                    return data;
                }
            }
        }

    }
}