using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;

namespace ESBackend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PinfoController : ControllerBase
    {
        private static string Ip {get; set;}
        private static DateTime LastUpdate {get; set;}

        // GET api/values
        [HttpGet]
        public ActionResult<string> Get()
        {
            return $"{Ip}\nLast update: {LastUpdate}Z" ?? "No IP has been provided.";
        }

        [HttpPost]
        public void Post([FromQuery] string ip)
        {
            Ip = ip;
            LastUpdate = DateTime.UtcNow;
        }
    }
}