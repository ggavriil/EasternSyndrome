using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;

namespace ESBackend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PingController : ControllerBase
    {
        private static string Ip {get; set;}
        private static DateTime LastUpdate {get; set;}

        [HttpGet]
        public ActionResult<string> Get()
        {
            return "Hello there!";
        }
    }
}