using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using ESFrontend.DataContract;
using Flurl;
using Flurl.Http;
using Newtonsoft.Json;

namespace ESFrontend.Models
{
    class SlouchGraphModel
    {
        public List<Tuple<DateTime, double>> Points {get; set;}
/*
        public SlouchGraphModel() {
            int numberOfDays = 7;
            var points = new List<Tuple<int, int>>();
            Random random = new Random();
            for(int i = 0; i < numberOfDays; i++) {
                points.Add(Tuple.Create(i, random.Next()));
            }
            Points = points;
        }
*/
        public SlouchGraphModel(int numberOfDays)
        {
            DateTime to = DateTime.Now;
            DateTime from = to.Subtract(new TimeSpan(numberOfDays, 0, 0, 0));
            var dataPoints = GetData(from, to);
            Points = dataPoints.Select(p => Tuple.Create(p.Timestamp, p.Angle)).ToList();
        }

        private IEnumerable<DeviceData> GetData(DateTime from, DateTime to)
        {
            var result = "http://es.giorgos.io:8080/api/devicedata".SendJsonAsync(HttpMethod.Get, new {From = from, To = to}).ReceiveString();
            var deserialised = JsonConvert.DeserializeObject<List<DeviceData>>(result.Result);
            return deserialised;
        }


    }
}