using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;

namespace ESBackend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class Notifications : ControllerBase
    {

        // GET api/values
        [HttpGet]
        public ActionResult<string> Get()
        {
            return "Hello!";
        }

        [HttpPost]
        public void Post([FromBody] int nid)
        {
            //Do things
        }
    }
}