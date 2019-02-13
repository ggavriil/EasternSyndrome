using System;
using System.Collections.Generic;

namespace ESFrontend.Models
{
    class SlouchGraphModel
    {
        public List<Tuple<int, int>> Points {get; set;}

        public SlouchGraphModel(int numberOfDays) {
            var points = new List<Tuple<int, int>>();
            Random random = new Random();
            for(int i = 0; i < numberOfDays; i++) {
                points.Add(Tuple.Create(i, random.Next()));
            }
            Points = points;
        }
    }
}