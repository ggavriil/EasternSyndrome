using System;
using System.Collections.Generic;
using ESBackend.DataContract;

namespace ESBackend
{
    public interface IDatabaseConnector
    {
        void InsertDeviceData(double angle, double accel, DateTime timestamp);
        IEnumerable<DeviceData> SelectDeviceData(DateTime from, DateTime to);
    }
}