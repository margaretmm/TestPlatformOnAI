/**
 * 压缩文件处理
 * @author maoyeqin
 * @throws IOException
 * @date 2017年5月27日下午4:03:29
 */
package utils;


import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
import org.apache.commons.compress.archivers.tar.TarArchiveInputStream;
import org.apache.commons.compress.compressors.gzip.GzipCompressorInputStream;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;

import javax.servlet.http.HttpServletRequest;
import java.io.*;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class FileHander {
    private static Logger logger = LoggerFactory.getLogger(FileHander.class);

    private static int bufferLen=1024;
    public static int getBufferLen() {
        return bufferLen;
    }

    private static String getTarDir(String ip){
        if (OSchecker.isOSLinux()){
            return "./target/download/"+ip+"/";
        }else{
            return ".\\target\\download\\"+ip+"\\";
        }
    }

    /**
     * create by: maoyeqin
     * description:
     * create time: 17:06 2018/7/17
     * 
      * @Param: null
     * @return 
     */
    public static String TarFileRecive(String ip,HttpServletRequest request){
        List<MultipartFile> files = ((MultipartHttpServletRequest) request).getFiles("file");
        MultipartFile file = null;
        BufferedOutputStream stream = null;
        for (int i = 0; i < files.size(); ++i) {
            file = files.get(i);
            String filePath =getTarDir(ip);
            File fileDir=new File(filePath);
            if (judeDirExists(fileDir)) {
                if (!file.isEmpty()) {
                    try {
                        File tarFile = new File(filePath + file.getOriginalFilename());
                        byte[] bytes = file.getBytes();
                        stream = new BufferedOutputStream(new FileOutputStream(tarFile));//设置文件路径及名字
                        stream.write(bytes);// 写入
                        stream.close();
                        unCompressArchiveGz(filePath + file.getOriginalFilename());
                    } catch (Exception e) {
                        stream = null;
                        logger.error( "第 " + i + " 个文件获取失败 ==> "+ e.getMessage());
                        return "第 " + i + " 个文件获取失败 ==> "+ e.getMessage();

                    }
                } else {

                    logger.error( "第 " + i + " 个文件获取失败因为文件为空");
                    return "第 " + i + " 个文件获取失败因为文件为空";
                }
            }
        }
        ImgRecognize.ImgRec(ip);
        return "获取成功";
    }

    /**
     * create by: maoyeqin
     * description:
     * create time: 17:06 2018/7/17
     * 
      * @Param: null
     * @return 
     */
    @Override
    protected void finalize() throws Throwable {
        super.finalize();
    }

    private static boolean judeDirExists(File file) {
        if (file.exists()) {
            if (file.isDirectory()) {
                logger.info( "dir exists");
                //System.out.println("dir exists");
                return true;
            } else {
                //System.out.println("the same name file exists, can not create dir");
                logger.error("the same name file exists, can not create dir");
                return false;
            }
        } else {
            //System.out.println("dir not exists, create it ...");
            logger.info( "dir not exists, create it ...");
            boolean a=file.mkdir();
            return a;
        }
    }

    /**
     * create by: maoyeqin
     * description:
     * create time: 17:06 2018/7/17
     * 
      * @Param: null
     * @return 
     */
    public static String getRemoteIp(HttpServletRequest request) {
        String ip = request.getHeader("X-Forwarded-For");
        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("Proxy-Client-IP");
        }
        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("WL-Proxy-Client-IP");
        }
        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("HTTP_CLIENT_IP");
        }
        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("HTTP_X_FORWARDED_FOR");
        }
        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getRemoteAddr();
        }
        return ip;
    }


/**
 * create by: maoyeqin
 * description:
 * create time: 17:07 2018/7/17
 * 
  * @Param: null
 * @return 
 */
    private static void unCompressArchiveGz(String archive) throws IOException {
        //int bufferLen=1024;
        File file = new File(archive);

        BufferedInputStream bis =
                new BufferedInputStream(new FileInputStream(file));

        String fileName =
                file.getName().substring(0, file.getName().lastIndexOf("."));

        String finalName = file.getParent() + File.separator + fileName;

        BufferedOutputStream bos =
                new BufferedOutputStream(new FileOutputStream(finalName));

        GzipCompressorInputStream gcis =
                new GzipCompressorInputStream(bis);

        byte[] buffer = new byte[getBufferLen()];
        int read = -1;
        while((read = gcis.read(buffer)) != -1){
            bos.write(buffer, 0, read);
        }
        gcis.close();
        bos.close();

        unCompressTar(finalName);
    }


    private static void unCompressTar(String finalName) throws IOException {

        File file = new File(finalName);
        String parentPath = file.getParent();
        TarArchiveInputStream tais =
                new TarArchiveInputStream(new FileInputStream(file));

        TarArchiveEntry tarArchiveEntry = null;

        while((tarArchiveEntry = tais.getNextTarEntry()) != null){
            String name = tarArchiveEntry.getName();
            File tarFile = new File(parentPath, name);
            if(!tarFile.getParentFile().exists()){
                tarFile.getParentFile().mkdirs();
            }

            BufferedOutputStream bos =
                    new BufferedOutputStream(new FileOutputStream(tarFile));

            int read = -1;
            byte[] buffer = new byte[getBufferLen()];
            while((read = tais.read(buffer)) != -1){
                bos.write(buffer, 0, read);
            }
            bos.close();
        }
        tais.close();
        file.delete();//删除tar文件
    }
}
