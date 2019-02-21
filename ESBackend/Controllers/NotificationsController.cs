using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Apache.NMS;
using Apache.NMS.ActiveMQ.Commands;
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
            Console.WriteLine("------------------ Received");
            Uri connecturi = new Uri("activemq:tcp://es.giorgos.io:61616");
            IConnectionFactory factory = new Apache.NMS.ActiveMQ.ConnectionFactory(connecturi);
            using(IConnection connection = factory.CreateConnection())
            using(ISession session = connection.CreateSession())
            {
                ActiveMQTopic topic = new ActiveMQTopic("VirtualTopic/ESNOTIF");
                using(IMessageProducer producer = session.CreateProducer(topic))
                {
                    // Start the connection so that messages will be processed.
                    connection.Start();
                    producer.DeliveryMode = MsgDeliveryMode.Persistent;
                    ITextMessage request = session.CreateTextMessage("Notification Received");
                    producer.Send(request);
                }
            }
        }
    }
}