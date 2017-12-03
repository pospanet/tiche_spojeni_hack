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

            foreach (DirectoryInfo characterFolder in directoryInfo.EnumerateDirectories())
            foreach (FileInfo fileInfo in characterFolder.EnumerateFiles("*.tsv"))
            {
                string label = characterFolder.Name;
                using (StreamWriter streamWriter = File.CreateText(Path.Combine(directoryInfo.FullName,
                    string.Concat(Path.GetFileNameWithoutExtension(fileInfo.FullName), ".labels.tsv"))))
                {
                    streamWriter.Write(label);
                }
            }
        }
    }
}