        package utils;

        import org.slf4j.Logger;
        import org.slf4j.LoggerFactory;
        import org.tensorflow.*;
        import org.tensorflow.types.UInt8;

        import java.io.*;
        import java.nio.charset.Charset;
        import java.nio.file.Files;
        import java.nio.file.Path;
        import java.nio.file.Paths;
        import java.util.Arrays;
        import java.util.List;

        /** Sample use of the TensorFlow Java API to label images using a pre-trained model. */
        public class ImgRecognize {
            private static Logger logger = LoggerFactory.getLogger(ImgRecognize.class);

            private static String modelDir=".\\target\\model";
            private static String modeName="tensorflow_inception_graph_new.pb";
            private static String testDataSetDir=null;
            private static String predictionFile=null;

            public static String getTestDataSetDir() {
                return testDataSetDir;
            }

            public static void setTestDataSetDir(String IP) {
                ImgRecognize.testDataSetDir = ".\\target\\download\\"+IP+"\\test\\";
            }

            public static String getPredictionFile() {
                return predictionFile;
            }

            public static void setPredictionFile(String IP) {
                ImgRecognize.predictionFile = ".\\target\\download\\"+IP+"\\prediction.csv";;
            }


            public static void main(String[] args) {
                //File directory = new File(".");
                //directory.getAbsolutePath();    //得到的是C:/test/.
                if (args.length < 2) {
                    logger.error("input para invalid!");
                    return;
                }
                ImgRec(args[1]);
            }

            public static void ImgRec(String IP){
                setTestDataSetDir(IP);
                setPredictionFile(IP);

                byte[] graphDef = readAllBytesOrExit(Paths.get(modelDir, modeName));
                List<String> labels =
                        readAllLinesOrExit(Paths.get(modelDir, "labels.txt"));

                File dir = new File(getTestDataSetDir());
                File[] files = dir.listFiles();

                File prediction = new File(getPredictionFile());
                try {
                    PrintStream ps = new PrintStream(new FileOutputStream(prediction));
                    if (files != null) {
                        for (File f1 : files) {
                            byte[] imageBytes = readAllBytesOrExit(Paths.get("" + f1));

                            try (Tensor<String> image = constructAndExecuteGraphToNormalizeImage_str(imageBytes)) {
                                float[] labelProbabilities = executeInceptionGraph(graphDef, image);
                                int bestLabelIdx = maxIndex(labelProbabilities);
                                System.out.println(
                                        String.format("%s BEST MATCH: %s (%.2f%% likely)",
                                                f1,
                                                labels.get(bestLabelIdx),
                                                labelProbabilities[bestLabelIdx] * 100f));

                                ps.append(String.format("%s %s %.2f%%\n",
                                        f1,
                                        labels.get(bestLabelIdx),
                                        labelProbabilities[bestLabelIdx] * 100f));// 在已有的基础上添加字符串
                            }
                        }
                    }
                }catch (FileNotFoundException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }

            private static Tensor<String> constructAndExecuteGraphToNormalizeImage_str(byte[] imageBytes) {
                try (Graph g = new Graph()) {
                    GraphBuilder b = new GraphBuilder(g);

                    // Since the graph is being constructed once per execution here, we can use a constant for the
                    // input image. If the graph were to be re-used for multiple input images, a placeholder would
                    // have been more appropriate.
                    final Output<String> input = b.constant("input", imageBytes);

                    try (Session s = new Session(g)) {
                        // Generally, there may be multiple output tensors, all of them must be closed to prevent resource leaks.
                        return s.runner().fetch(input.op().name()).run().get(0).expect(String.class);
                    }
                }
            }

            private static float[] executeInceptionGraph(byte[] graphDef, Tensor<String> image) {
                try (Graph g = new Graph()) {
                    g.importGraphDef(graphDef);
                    //System.out.print("~~~~"+g.operation("DecodeJpeg/contents").type()+"\\r\\n");
                    try (Session s = new Session(g);
                         // Generally, there may be multiple output tensors, all of them must be closed to prevent resource leaks.
                         Tensor<Float> result =
                                 s.runner().feed("DecodeJpeg/contents:0", image).fetch("output/prob").run().get(0).expect(Float.class)) {
                        final long[] rshape = result.shape();
                        if (result.numDimensions() != 2 || rshape[0] != 1) {
                            throw new RuntimeException(
                                    String.format(
                                            "Expected model to produce a [1 N] shaped tensor where N is the number of labels, instead it produced one with shape %s",
                                            Arrays.toString(rshape)));
                        }
                        int nlabels = (int) rshape[1];
                        return result.copyTo(new float[1][nlabels])[0];
                    }
                }
            }

            private static int maxIndex(float[] probabilities) {
                int best = 0;
                for (int i = 1; i < probabilities.length; ++i) {
                    if (probabilities[i] > probabilities[best]) {
                        best = i;
                    }
                }
                return best;
            }

            private static byte[] readAllBytesOrExit(Path path) {
                try {
                    return Files.readAllBytes(path);
                } catch (IOException e) {
                    System.err.println("Failed to read [" + path + "]: " + e.getMessage());
                    System.exit(1);
                }
                return null;
            }

            private static List<String> readAllLinesOrExit(Path path) {
                try {
                    return Files.readAllLines(path, Charset.forName("UTF-8"));
                } catch (IOException e) {
                    System.err.println("Failed to read [" + path + "]: " + e.getMessage());
                    System.exit(0);
                }
                return null;
            }

            // In the fullness of time, equivalents of the methods of this class should be auto-generated from
            // the OpDefs linked into libtensorflow_jni.so. That would match what is done in other languages
            // like Python, C++ and Go.
            static class GraphBuilder {
                GraphBuilder(Graph g) {
                    this.g = g;
                }

                Output<Float> div(Output<Float> x, Output<Float> y) {
                    return binaryOp("Div", x, y);
                }

                <T> Output<T> sub(Output<T> x, Output<T> y) {
                    return binaryOp("Sub", x, y);
                }

                <T> Output<Float> resizeBilinear(Output<T> images, Output<Integer> size) {
                    return binaryOp3("ResizeBilinear", images, size);
                }

                <T> Output<T> expandDims(Output<T> input, Output<Integer> dim) {
                    return binaryOp3("ExpandDims", input, dim);
                }

                <T, U> Output<U> cast(Output<T> value, Class<U> type) {
                    DataType dtype = DataType.fromClass(type);
                    return g.opBuilder("Cast", "Cast")
                            .addInput(value)
                            .setAttr("DstT", dtype)
                            .build()
                            .<U>output(0);
                }

                Output<UInt8> decodeJpeg(Output<String> contents, long channels) {
                    return g.opBuilder("DecodeJpeg", "DecodeJpeg")
                            .addInput(contents)
                            .setAttr("channels", channels)
                            .build()
                            .<UInt8>output(0);
                }

                <T> Output<T> constant(String name, Object value, Class<T> type) {
                    try (Tensor<T> t = Tensor.<T>create(value, type)) {
                        return g.opBuilder("Const", name)
                                .setAttr("dtype", DataType.fromClass(type))
                                .setAttr("value", t)
                                .build()
                                .<T>output(0);
                    }
                }
                Output<String> constant(String name, byte[] value) {
                    return this.constant(name, value, String.class);
                }

                Output<Integer> constant(String name, int value) {
                    return this.constant(name, value, Integer.class);
                }

                Output<Integer> constant(String name, int[] value) {
                    return this.constant(name, value, Integer.class);
                }

                Output<Float> constant(String name, float value) {
                    return this.constant(name, value, Float.class);
                }

                private <T> Output<T> binaryOp(String type, Output<T> in1, Output<T> in2) {
                    return g.opBuilder(type, type).addInput(in1).addInput(in2).build().<T>output(0);
                }

                private <T, U, V> Output<T> binaryOp3(String type, Output<U> in1, Output<V> in2) {
                    return g.opBuilder(type, type).addInput(in1).addInput(in2).build().<T>output(0);
                }
                private Graph g;
            }
        }
