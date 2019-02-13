using System;
using System.Threading;
using Apache.NMS;
using Apache.NMS.ActiveMQ.Commands;
using Apache.NMS.Util;

namespace Apache.NMS.ActiveMQ.Test
{
    public class Program
    {
        protected static AutoResetEvent semaphore = new AutoResetEvent(false);
        protected static IMessage message = null;
        protected static TimeSpan receiveTimeout = TimeSpan.FromSeconds(1000);

        public static void Main(string[] args)
        {
            // Example connection strings:
            //    activemq:tcp://activemqhost:61616
            //    stomp:tcp://activemqhost:61613
            //    ems:tcp://tibcohost:7222
            //    msmq://localhost

            Uri connecturi = new Uri("activemq:tcp://es.giorgos.io:61616");

            Console.WriteLine("About to connect to " + connecturi);

            // NOTE: ensure the nmsprovider-activemq.config file exists in the executable folder.
            //IConnectionFactory factory = new NMSConnectionFactory(connecturi);
            IConnectionFactory factory = new Apache.NMS.ActiveMQ.ConnectionFactory(connecturi);
            using (IConnection connection = factory.CreateConnection())
            using (ISession session = connection.CreateSession())
            {
                // Examples for getting a destination:
                //
                // Hard coded destinations:
                //    IDestination destination = session.GetQueue("FOO.BAR");
                //    Debug.Assert(destination is IQueue);
                //    IDestination destination = session.GetTopic("FOO.BAR");
                //    Debug.Assert(destination is ITopic);
                //
                // Embedded destination type in the name:
                //    IDestination destination = SessionUtil.GetDestination(session, "queue://FOO.BAR");
                //    Debug.Assert(destination is IQueue);
                //    IDestination destination = SessionUtil.GetDestination(session, "topic://FOO.BAR");
                //    Debug.Assert(destination is ITopic);
                //
                // Defaults to queue if type is not specified:
                //    IDestination destination = SessionUtil.GetDestination(session, "FOO.BAR");
                //    Debug.Assert(destination is IQueue);
                //
                // .NET 3.5 Supports Extension methods for a simplified syntax:
                //    IDestination destination = session.GetDestination("queue://FOO.BAR");
                //    Debug.Assert(destination is IQueue);
                //    IDestination destination = session.GetDestination("topic://FOO.BAR");
                //    Debug.Assert(destination is ITopic);
                //IDestination destination = SessionUtil.GetDestination(session, "queue://Consumer.esb.VirtualTopic.es-data");
                //ActiveMQQueue topic = new ActiveMQQueue("Consumer.ERIC.VirtualTopic.ESDATA");
                ActiveMQTopic topic = new ActiveMQTopic("VirtualTopic/ESDATA");

                Console.WriteLine("Using destination: " + topic);

                // Create a consumer and producer
                using (IMessageConsumer consumer = session.CreateConsumer(topic))
                //using(IMessageProducer producer = session.CreateProducer(destination))
                {
                    // Start the connection so that messages will be processed.
                    connection.Start();
                    //producer.DeliveryMode = MsgDeliveryMode.Persistent;
                    //producer.RequestTimeout = receiveTimeout;

                    consumer.Listener += new MessageListener(OnMessage);

                    /*
                    // Send a message
                    ITextMessage request = session.CreateTextMessage("Hello World!");
                    request.NMSCorrelationID = "abc";
                    request.Properties["NMSXGroupID"] = "cheese";
                    request.Properties["myHeader"] = "Cheddar";

                    producer.Send(request);
                    */

                    while (true)
                    {
                        // Wait for the message
                        semaphore.WaitOne((int)receiveTimeout.TotalMilliseconds, true);
    
                        if (message == null)
                        {
                            Console.WriteLine("No message received!");
                        }
                        else
                        {
                            IBytesMessage bmsg = message as IBytesMessage;
                            Console.WriteLine("Received message with ID:   " + bmsg.NMSMessageId);
                            Console.WriteLine("Received message with text: " + System.Text.Encoding.UTF8.GetString(bmsg.Content));
                        }
                    }
                }
            }
        }

        protected static void OnMessage(IMessage receivedMsg)
        {
            message = receivedMsg as IMessage;
            semaphore.Set();
        }
    }
}