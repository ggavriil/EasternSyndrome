using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;

namespace ESBackend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class DeviceDataController : ControllerBase
    {

        private IDatabaseConnector dbConnector = new PgSqlDatabaseConnector();

        [HttpGet]
        public ActionResult<string> Get([FromBody] Interval interval)
        {
            var data = dbConnector.SelectDeviceData(interval.From, interval.To);
            return JsonConvert.SerializeObject(data.ToList());
        }

        public class Interval 
        {
            public DateTime From { get; set; }
            public DateTime To { get; set; }
        }

    }
}