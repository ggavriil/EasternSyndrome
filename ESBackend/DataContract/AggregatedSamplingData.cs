namespace ESBackend.DataContract
{
    public class AggregatedSamplingData
    {
        public int Size { get; set; }

        public double AdcV { get; set; }

        public SamplingData[] Samples { get; set; }

    }
}