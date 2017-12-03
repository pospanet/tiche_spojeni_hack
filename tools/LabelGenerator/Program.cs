using System.IO;
using System.Linq;

namespace LabelGenerator
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            string directoryPath = args.First(arg => arg.ToLower().StartsWith("dir:")).Replace("dir:", string.Empty);

            DirectoryInfo directoryInfo = new DirectoryInfo(directoryPath);

            foreach (FileInfo fileInfo in directoryInfo.EnumerateFiles("*.tsv"))
            {
                string label = fileInfo.Name.Split().First();
                using (StreamWriter streamWriter = File.CreateText(Path.Combine(directoryInfo.FullName,
                    string.Concat(Path.GetFileNameWithoutExtension(fileInfo.FullName), ".labels.tsv"))))
                {
                    streamWriter.Write(label);
                }
            }
        }
    }
}