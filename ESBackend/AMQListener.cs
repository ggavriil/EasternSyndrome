using System;
using System.Linq;
using System.Threading;
using Apache.NMS;
using Apache.NMS.ActiveMQ;
using Apache.NMS.ActiveMQ.Commands;
using Apache.NMS.Util;
using ESBackend.DataContract;
using Newtonsoft.Json;

namespace ESBackend
{
    public static class AMQListener
    {
        private static AutoResetEvent semaphore = new AutoResetEvent(false);
        private static IMessage message = null;
        private static TimeSpan receiveTimeout = TimeSpan.FromSeconds(1000000);

        public static void Listen()
        {
            IDatabaseConnector dbConnector = new PgSqlDatabaseConnector();
            Uri connecturi = new Uri("activemq:tcp://es.giorgos.io:61616");
            Console.WriteLine("About to connect to " + connecturi);

            // NOTE: ensure the nmsprovider-activemq.config file exists in the executable folder.
            //IConnectionFactory factory = new NMSConnectionFactory(connecturi);
            IConnectionFactory factory = new Apache.NMS.ActiveMQ.ConnectionFactory(connecturi);
            using (IConnection connection = factory.CreateConnection())
            using (ISession session = connection.CreateSession())
            {

                //ActiveMQQueue topic = new ActiveMQQueue("Consumer.ERIC.VirtualTopic.ESDATA");
                ActiveMQTopic topic = new ActiveMQTopic("VirtualTopic/ESDATA");

                Console.WriteLine("Using destination: " + topic);

                using (IMessageConsumer consumer = session.CreateConsumer(topic))
                {
                    connection.Start();

                    consumer.Listener += new MessageListener(OnMessage);

                    while (true)
                    {
                        semaphore.WaitOne((int)receiveTimeout.TotalMilliseconds, true);
    
                        if (message == null)
                        {
                            Console.WriteLine("No message received!");
                        }
                        else
                        {
                            IBytesMessage bmsg = message as IBytesMessage;
                            Console.WriteLine("Received message with ID:   " + bmsg.NMSMessageId);
                            var jsonString = System.Text.Encoding.UTF8.GetString(bmsg.Content);
                            AggregatedSamplingData data = JsonConvert.DeserializeObject<AggregatedSamplingData>(jsonString);
                            foreach (var sample in data.Samples)
                            {
                               System.DateTime dtDateTime = new DateTime(1970,1,1,0,0,0,0,System.DateTimeKind.Utc);
                               dtDateTime = dtDateTime.AddSeconds(sample.Timestamp).ToUniversalTime();
                               dbConnector.InsertDeviceData(sample.MeanAngleZ, sample.StdAcc, dtDateTime); 
                            }
                            //Console.WriteLine("Received message with text: " + System.Text.Encoding.UTF8.GetString(bmsg.Content));
                        }
                    }
                }
            }
        }

        private static void OnMessage(IMessage receivedMsg)
        {
            message = receivedMsg as IMessage;
            semaphore.Set();
        }
        
    }
}