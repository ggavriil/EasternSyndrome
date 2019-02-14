using System;

namespace ESBackend.DataContract
{
    public class DeviceData
    {
        public int DeviceId { get; set; }
        public double Angle { get; set; }

        public double AccelStdDev { get; set; }
        public DateTime Timestamp { get; set; }

        public DeviceData(DateTime timestamp, double angle, double accel, int deviceid = 1) 
        {
            DeviceId = deviceid;
            Angle = angle;
            AccelStdDev = accel;
            Timestamp = timestamp;
        }

        public override string ToString() 
        {
            return $"({DeviceId}, {Angle}, {AccelStdDev}, {Timestamp})";
        }
    }
}