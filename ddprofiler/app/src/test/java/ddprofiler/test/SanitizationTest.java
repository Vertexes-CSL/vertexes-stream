package ddprofiler;

import static org.junit.Assert.assertTrue;

import org.junit.Test;

import ddprofiler.preanalysis.PreAnalyzer;

public class SanitizationTest {

    private String values =
            "160,124.08, 73,703.27, 100,553.38, 18,642.53, 48,622.24, 55,046.17, 26,966.05, 84,329.46, 260,390.37, 83,518.04, 27,424.07, 95,445.1, 36,794.62, 12,657.31, 5,784.7, 48,989.17, 13,590.41, 8,141.95, 1,396.85, 6,910.33, 46,574.18, 12,498.73, 167,922.77, 180, 2,030.11, 13,259.73, 4,827.23, 16,117.42, 86,521.66, 21,710.72, 4,667.7, 4,630.7, 73,432.63, 9,320.91, 121,649.77, 62,551.08, 25,173.77, 156,676.36, 405,033.97, 44,321.76, 9,766.11, 61,937.11, 144,673.42, 45,397.46, 382.61, 29,214.19, 7,760.09, 23,160.22, 18,690.22, 2,034.38, 960, 19,010.96, 12,634.2, 140, 36,051.39, 168,261.25, 12,942.63, 15,420.13, 4,686.42, 9,320.91, 162,614.16, 116,239.37, 21,022.71, 239,353.28, 145,819.4, 75,808.22, 26,078.68, 418,662.59, 88,826.92, 24,787.4, 112,799.19, 66,530.75, 143,950.12, 30,130.11, 41,397.61, 15,506.61, 16,137.29, 120,136.72, 85,812.19, 9,599.32, 2,649.3, 6,081.18, 454.61, 241.54, 15,136.28, 3,109.94, 12,421.75, 34,427.72, 109,397.67, 142.94, 114,713.44, 16,559.95, 4,653.21, 26,705.26, 51,146.78, 65,896.06, 154,515.73, 6,074.7, 133,545.12, 11,247.27, 23,656.67, 133,709.64, 1,680.39, 367,688.6, 149,742.43, 31,334.45, 143,032.14, 1,812.03, 49,933.39, 42,145.98, 52,869.94, 8,789.53, 6,766.98, 58,104.54, 2,225.34, 1,585.32, 128,989.56, 25,692.9, 132,006.46, 4,661.33, 4,667.7, 77,154, 18,501.98, 37,006.11, 463,662, 10,373.95, 16,118.61, 129,397.16, 24,988.56, 25,568.41, 101,813.25, 173,875.21, 20,795.59, 1,249.72, 2,925.3, 8,049.06, 9,215.4, 189,941.11, 5,339.35, 2,989.21, 18,635.38, 25,834.27, 9,271.12, 152,328.35, 4,635.79, 4,677.62, 4,687.15, 35,748.48, 13,995.47, 144,270.71, 102,832.84, 27,661.19, 7,979.62, 107,990.76, 172,309.33, 20,514.89, 46,633.25, 9,525.85, 55,607.34, 2,644.67, 881.78, 9,060.39, 42,922.56, 21,163.64, 132.03, 2,200.92, 186,998.09, 133,099.42, 183,162, 12,611.59, 2,835, 3,670.03, 82,480.74, 14,909.35, 183,168.57, 116,213.91, 133,732.1, 77,685.93, 68,012.32, 79,050.49, 143,681.84, 39,121.04, 57,227.15, 5,889.33, 74,098.19, 71,648.86, 10,084.86, 44,980.93, 5,882.04, 33,044.91, 50,148.39, 252,835.49, 39,469.53, 362,686.82, 400.94, 1,469.02, 122,080.04, 1,159.47, 117, 13,367.83, 17,991.16, 17,792.83, 2,300.01, 80,942.35, 75,800.06, 5,013.14, 26,411.82, 64,847.33, 120,331.42, 106,714.57, 132,529.78, 31,093.51, 103,874.44, 13,810.89, 3,058.54, 71,443.5, 12,634.2, 11,664.6, 17,286.8, 12,634.2, 191,189.7, 24,005.53, 115,603.99, 4,653.21, 42,145.75, 13,983.54";
    private String values1 =
            "103,996.2, 46,456.73, 50,488.32, 11,190.61, 34,500.48, 36,106.19, 14,686.51, 56,162.59, 155,115.84, 54,118.17, 15,923.57, 63,274.76, 26,289.14, 10,379.88, 5,291.98, 39,224.66, 7,922.29, 7,683.4, 1,220.02, 4,364.63, 26,203.69, 7,647.77, 105,084.27, 0, 1,849.2, 9,419.74, 4,368.53, 9,815.14, 71,925.83, 16,613.48, 3,713.09, 3,701.56, 48,459.39, 7,417.78, 74,023.09, 46,725.98, 15,513.88, 90,313.13, 275,824.7, 37,130.01, 0, 47,134.54, 102,850.31, 27,673.54, 311.78, 17,229.44, 7,211.92, 19,138.64, 18,153.93, 1,617.25, 912.58, 9,825.59, 7,792.77, 121.25, 24,907.62, 96,220.02, 9,429.93, 9,087.92, 3,725.83, 7,417.78, 99,520.02, 76,126.94, 15,903.62, 219,268.15, 71,541.2, 39,252.86, 20,063.87, 218,676.63, 53,929.74, 17,041.11, 68,809.22, 48,402.5, 86,926.62, 12,814.87, 38,065.91, 14,099.82, 14,768.86, 65,000.32, 50,160.21, 5,216.46, 1,891.48, 5,375.22, 372.3, 188.14, 9,683.6, 2,815.19, 8,671.97, 32,379.24, 82,318.33, 112.5, 68,572.31, 10,291.38, 3,704.69, 18,689.54, 16,257.6, 37,251.65, 103,712.5, 5,585.84, 80,689.29, 0, 14,584.37, 71,189.32, 643.66, 201,064.99, 100,796.84, 0, 129,868.34, 439.51, 34,857.85, 20,461.58, 42,666.46, 6,630.71, 5,452.11, 31,838.33, 2,062.22, 0, 66,832.71, 24,982.22, 82,568.84, 3,701.95, 3,713.09, 50,572.78, 14,974.7, 20,980.09, 286,126.22, 5,443.11, 11,616.3, 69,136.19, 16,833.91, 18,125.96, 65,273.27, 74,368.15, 17,407.77, 0, 155.39, 4,586.56, 7,989.19, 107,518.76, 2,815.91, 2,567.45, 14,812.52, 16,761.01, 6,152.18, 108,852.71, 3,705.6, 3,727.52, 3,721.22, 20,108.52, 11,150.3, 86,437.63, 55,961.51, 21,650.24, 6,906.99, 52,259.96, 120,517.81, 18,402.12, 41,521.21, 8,260.29, 40,136.19, 2,299.14, 794.16, 7,042.49, 32,925.58, 13,246.98, 116.25, 1,282.67, 180,438.3, 77,423.81, 116,165.53, 8,364.37, 2,463.75, 1,441.36, 47,859.73, 7,684, 96,632.08, 57,877.47, 75,600.39, 49,904.03, 41,662.46, 4,380, 78,115.52, 22,725.98, 38,547.18, 4,450.4, 63,702.43, 66,681.39, 8,107.66, 32,644.6, 5,345.16, 29,070.51, 31,346.41, 157,640.89, 25,567.13, 251,368.74, 348.95, 1,469.03, 76,299.23, 694.95, 91.07, 9,321.57, 11,582.66, 11,318.81, 2,300, 55,175.35, 36,377.74, 2,850.15, 16,932.94, 35,966.75, 79,388.35, 71,240.6, 82,366.87, 28,091.01, 71,520.42, 10,426.98, 2,225.79, 53,401.65, 7,792.1, 6,716.63, 10,707.53, 7,793.07, 94,044.5, 12,993.85, 84,270.83, 3,704.69, 37,495.92, 11,133.38";
    private String values2 =
            "40,872.88, 20,716.29, 36,744.91, 4,967.95, 10,286.49, 13,256.26, 9,130.02, 19,888.56, 81,508.71, 21,512.29, 8,443.21, 25,295.16, 0, 797.4, 0, 5,633.88, 4,152.3, 143.22, 30.67, 1,851.64, 15,253.71, 2,760.68, 37,556.34, 151.33, 30.67, 1,558.98, 24.48, 4,323.58, 7,996.01, 3,721.46, 454.55, 451.91, 17,436.67, 904.31, 35,800.09, 10,909.03, 7,215.29, 47,636.33, 94,063.48, 708.42, 8,652.37, 9,708.52, 31,170.35, 12,292, 0, 6,961.62, 0, 1,981.35, 0, 0, 0, 5,593.55, 2,746.05, 0, 6,977.47, 42,410.16, 1,286.86, 4,310.49, 453.68, 904.31, 45,693.93, 28,750.63, 3,372.01, 10,269.82, 58,647.1, 29,975.58, 4,361.8, 152,625.73, 22,654.76, 5,242, 34,603.82, 12,395.52, 40,977.5, 12,813.65, 222.51, 205.19, 277.79, 44,783.75, 23,182.63, 2,751.42, 16.82, 11.05, 13.64, 2.51, 3,351.5, 0, 2,463.49, 594.57, 20,654.76, 0, 32,718.09, 4,232.84, 449.76, 4,780.91, 27,693.04, 20,781.15, 38,432.75, 263.41, 42,174.51, 11,247.27, 6,483.26, 46,871.43, 874.79, 124,244.34, 37,569.45, 25,029.45, 5,780.48, 0, 9,710.88, 17,716.79, 6,075.51, 0, 715.94, 7,768.58, 0, 1,180.83, 43,402.05, 0, 34,134.47, 454.98, 454.55, 18,936.55, 2,388.47, 11,550.51, 121,288.13, 4,097.66, 2,717.2, 43,636.05, 5,711.41, 4,960.76, 23,848.53, 83,282.61, 873.91, 1,160.58, 2,705.41, 0, 239.41, 43,591.64, 1,959.77, 151.48, 2,425.79, 6,385.23, 1,249.23, 26,869.84, 453.68, 445.9, 460.59, 11,871.58, 1,358.4, 42,481.65, 32,516.91, 1,390.09, 303.46, 42,972.01, 28,758.1, 117.63, 2,815.06, 0, 4,760.49, 0, 0.03, 849.63, 4,266.76, 5,884.84, 0, 0, 3,238.58, 41,632.04, 55,856.44, 1,783.51, 92.98, 1,972.51, 24,859.8, 4,956.87, 71,677.19, 46,857.95, 41,247.92, 21,022.23, 18,804.23, 67,876.13, 50,275.36, 10,516.52, 11,260.64, 909.69, 2,118.35, 349.28, 631.93, 8,418.18, 160.86, 260.02, 14,440.37, 58,073.35, 7,590.42, 63,800.8, 0, 0, 36,416.07, 259.08, 0, 2,817.74, 4,275.18, 4,366.68, 0, 16,513.26, 29,421.17, 1,777.63, 6,760.5, 18,560.3, 31,947.68, 24,575.99, 31,273.3, 424.97, 21,215.67, 1,578.19, 218.06, 9,744.51, 2,728.18, 2,614.09, 3,946.3, 2,848.45, 68,008.19, 8,551.16, 25,211.66, 449.76, 2,824.04, 1,362.34";
    private String values3 =
            "766,332.16672, 767,433.66957, 766,118.33409, 767,799.54882, , 765,965.67766, 766,449.0276, 766,341.43468, 767,343.49146, 767,547.05603, 768,069.70518, 768,708.09015, 768,740.19956, 766,234.21735, 764,691.4041, 764,351.12835, 766,025.78985, , 658,688.02823, , 765,591.99335, , 764,789.5372, , , , , , 763,036.44851, 765,141.26844, , , 767,480.06446, 763,216.46723, 766,931.08927, 766,150.16447, , 767,799.8444, 768,961.13218, 768,398.03607, 765,792.03738, 764,988.8891, 764,844.19426, 764,507.70102, , 739,102.39365, 796,355.41193, , , 658,888.89276, , 765,605.05647, , 765,106.01836, 764,400.30265, 764,405.97842, , , , 763,310.04989, 766,685.70812, 766,344.62904, , , 766,525.17993, 766,238.79192, 765,852.662, 766,530.28538, 766,856.28273, , 767,571.81186, 768,088.49022, 768,686.08396, 769,090.96655, , , 764,747.98736, 764,508.0171, 764,285.32651, 765,945.06405, , 796,100.29527, 795,443.12177, , 738,903.0968, 660,483.31698, , 765,365.72624, 765,215.96003, , 764,140.06982, , , 766,229.8478, 766,752.96513, 766,744.90512, 767,167.92839, 766,034.06508, 766,665.28283, , , 767,239.13493, 766,797.02686, 767,170.13363, 767,528.03043, 765,877.28985, 766,223.39595, 922.3372, 765,123.30905, 765,614.61178, , , 795,922.70284, 795,775.03719, , , 765,787.85673, 764,874.46958, 763,765.44724, , , 767,333.95523, 766,116.10803, , 766,821.93193, 766,108.42288, 766,307.82009, 767,159.9448, , , 767,886.80827, 767,698.51797, , 765,833.84857, 765,761.41181, , , 766,033.6849, 765,866.43793, , , , , 763,344.84497, , , , 763,089.02705, 763,431.30458, 766,433.95508, 766,099.50817, 768,196.98498, 768,061.42548, 768,465.93793, 768,621.58021, , 764,586.83377, 922.3372, , , 660,292.40228, 657,854.40782, 659,331.98663, , , , 764,925.65477, 765,418.63265, 765,689.59945, , , , 762,489.85176, 763,020.16356, 766,288.88214, 766,817.4179, 767,026.5576, 766,432.72732, 765,889.03725, 766,026.05419, 767,014.32081, 766,938.54517, 766,794.3374, 767,594.41678, 766,274.78568, 766,129.53298, 765,503.66082, 764,912.91509, 765,573.01373, 768,278.21793, 764,622.8361, 763,888.73286, 764,735.81396, 763,676.49545, , , 765,426.41104, 764,996.70269, , , , , 762,572.95558, 766,190.50562, 766,016.18442, , , 767,825.21787, 767,616.12841, 768,367.39925, 764,778.56585, , 765,031.70746, 796,055.78876, 796,445.14395, 765,582.19012, , , 765,027.6508, , 763,869.57443, , 763,403.67751, , 761,724.03371, 763,229.88142";
    private String values4 =
            "10,286.49, 152,699.33, 83,752.67, 21,499.9, 34,733.83, 9,710.88, 1,160.58, 239.41, 6,156.84, 0, 30.67, 151.48, 1,851.64, 17,716.79, 55,856.44, 1,289.78, 32,792.85, 1,972.51, 16,728.77, 20,719.31, 14,274.26, 10,269.82, 32,519.06, 29,949.69, 11,247.27, 47,623.46, 95,303.04, 632.03, 13,088.45, 873.91, 12,314.36, 260.02, 0, 23,182.63, 63,800.8, 7,529.01, 2,742.54, 92.98, 0, 4,385.7, 7,904.77, 445.9, 1,358.4, 35,902.05, 27,824.36, 1,777.63, 10,909.03, 48,293.13, 18,156.46, 37,489.53, 43,082.81, 40,977.5, 25,153.08, 29,645.23, 25,029.45, 8,652.37, 14,440.37, 8,419.29, 21,271.39, 37.84, 44,698.29, 16.82, 1,578.19, 218.06, 43,357.57, 13.64, 0, 0, 849.63, 5,586.45, 151.33, 30.67, 0, 25,211.66, 453.68, 454.98, 451.91, 18,936.55, 904.31, 28,714.12, 40,740.68, 42,200.19, 4,787.15, 42,202.87, 40,382.82, 9,148.25, 18,801.94, 19,933.08, 4,097.66, 11,260.64, 909.69, 152.18, 0, 2,705.41, 5,780.48, 0, 5,534.67, 6,075.51, 6,961.62, 0, 11.05, 0, 0, 2,463.49, 0, 2,879.06, 1,778.93, 67,667.38, 454.55, 454.55, 1,362.34, 904.31, 463.83, 11,550.51, 0, 424.97, 30,884.31, 4,152.3, 43,493.47, 4,760.49, 0, 15,253.71, 594.57, 20,654.76, 0, 6,977.47, 25,043.7, 4,956.87, 2,388.47, 28,964.52, 121,735.52, 58,854.35, 2,717.2, 22,701.76, 5,242, 874.79, 32,381.88, 12,395.89, 1,390.09, 708.42, 2,815.06, 153.75, 0, 0, 2,086.13, 797.4, 715.94, 0, 41,632.04, 143.22, 2.51, 3,351.5, 5,884.84, 0, 1,889.57, 2,749.42, 2,861.81, 2,737.87, 42,726.77, 34,134.47, 8,379.57, 4,187.49, 4,498.52, 11,871.58, 2,824.04, 3,721.46, 453.68, 449.76, 449.76, 45,067.5, 36,508.04, 71,775.17, 4,267.86, 67,876.13, 42,058.15, 6,483.26, 5,711.41, 80,655.18, 124,585.07, 303.46, 8,443.21, 349.28, 31,273.3, 9,575.28, 277.79, 58,073.35, 7,590.42, 1,981.35, 0, 4,266.76, 36,416.07, 37,556.34, 9,744.51, 2,844.4, 1,564.62, 1,247.18, 24.48, 2,817.74, 4,274.43, 460.59, 17,436.67, 20,859.74, 4,967.95, 38,225.86, 3,372.01, 47,073.19, 21,121.3, 263.41, 13,256.26, 50,261.23, 10,516.52, 6,760.5, 4,960.76, 7,215.29, 23,768.81, 24,569.11, 117.63, 0, 0.03, 2,425.79, 1,180.83, 6,385.23, 3,238.58, 3,946.3, 259.08, 0, 0, 4,458.48, 26,785.79, 28,714.12, 35,902.05, 40,757.84, 45,067.5, 16,728.77, 22,701.76, 36,508.04, 20,859.74, 28,964.52, 42,183.9, 4,787.15, 14,274.26, 71,775.17, 38,225.86, 47,073.19, 263.41, 40,382.82, 21,121.3, 42,202.87, 10,909.03, 121,735.52, 13,256.26, 9,148.25, 18,801.94, 58,854.35, 32,519.06, 19,933.08, 29,949.69, 4,267.86, 67,876.13, 4,097.66, 2,717.2, 152,699.33, 11,260.64, 20,719.31, 909.69, 43,587.86, 50,261.23, 10,516.52, 18,936.55, 17,436.67, 47,767.86, 80,655.18, 874.79, 27,824.36, 124,585.07, 2,388.47, 4,967.95, 18,156.46, 5,780.48, 153.75, 43,357.57, 2,749.42, 43,493.47, 5,586.45, 41,632.04, 3,721.46, 67,667.38, 26,785.79, 25,211.66, 4,956.87, 11,871.58, 7,904.77, 25,043.7, 117.63, 424.97, 8,652.37, 1,160.58, 2,705.41, 260.02, 37.84, 0, 0, 239.41, 2,086.13, 797.4, 349.28, 873.91, 31,273.3, 9,710.88, 9,575.28, 30,884.31, 277.79, 14,440.37, 12,314.36, 0, 44,698.29, 5,534.67, 23,182.63, 463.83, 3,372.01, 11,550.51, 10,286.49, 1,777.63, 10,269.82, 11,247.27, 6,760.5, 4,960.76, 7,215.29, 6,483.26, 5,242, 5,711.41, 83,752.67, 32,381.88, 21,499.9, 34,634.14, 37,552.68, 23,768.81, 47,623.46, 303.46, 8,443.21, 12,395.89, 1,390.09, 24,569.11, 708.42, 43,086.97, 40,977.5, 25,153.08, 29,645.23, 13,088.45, 95,303.04, 0, 152.18, 632.03, 25,029.45, 8,419.29, 21,271.39, 2,815.06, 6,961.62, 0, 4,152.3, 6,156.84, 1,889.57, 17,716.79, 55,856.44, 9,744.51, 15,253.71, 594.57, 20,654.76, 36,416.07, 3,238.58, 37,556.34, 0, 92.98, 30.67, 6,977.47, 42,726.77, 2,817.74, 32,792.85, 34,134.47, 4,267.86, 67,876.13, 4,097.66, 2,717.2, 152,699.33, 11,260.64, 20,719.31, 909.69, 43,587.86, 50,261.23, 10,516.52, 18,936.55, 17,436.67, 47,012.55, 80,678.71, 874.79, 27,824.36, 124,585.07, 2,388.47, 4,967.95, 18,156.46, 5,780.48, 153.75, 43,357.57, 2,749.42, 43,493.47, 5,586.45, 41,632.04, 3,721.46, 58,073.35, 7,590.42, 63,800.8, 0, 3,351.5, 0, 0, 0.03, 0, 849.63, 4,266.76, 30.67, 5,884.84, 2,425.79, 2,463.49, 6,385.23, 1,851.64, 0, 3,946.3, 259.08, 0, 151.33, 0, 0, 2,879.06, 2,861.81, 2,844.4, 2,742.54, 2,737.87, 1,778.93, 1,289.78, 1,564.62, 1,247.18, 24.48, 8,379.57, 4,187.49, 4,274.43, 4,458.48, 4,385.7, 4,498.52, 1,972.51, 453.68, 453.68, 454.98, 454.55, 449.76, 454.55, 449.76, 445.9, 451.91, 460.59, 2,824.04, 0, 0, 6,075.51, 16.82, 715.94, 1,578.19, 11.05, 0, 218.06, 7,768.58, 13.64, 1,981.35, 0, 4,760.49, 0, 0, 143.22, 2.51, 151.48, 1,180.83, 0, 0, 904.31, 904.31, 0, 1,362.34, 1,358.4, 463.83, 3,372.01, 11,550.51, 10,286.49, 1,777.63, 10,269.82, 11,247.27, 6,760.5, 4,960.76, 7,215.29, 6,483.26, 5,242, 5,711.41";

    @Test
    public void sanitizeTest() {
        String test = "";
        String test2 = " ";
        String test3 = "   ";

        String tc = test.trim().toLowerCase();
        String tc2 = test.trim().toLowerCase();
        String tc3 = test.trim().toLowerCase();

        assertTrue(tc.equals(""));
        assertTrue(tc2.equals(""));
        assertTrue(tc3.equals(""));

        // parsing commas

        String value = "160,124.08";
        String value2 = "-71.0924";
        String value3 = "23.4353543";
        String value4 = "234,234.54";
        boolean num = PreAnalyzer.isNumerical(value);
        boolean num2 = PreAnalyzer.isNumerical(value2);
        boolean num3 = PreAnalyzer.isNumerical(value3);
        boolean num4 = PreAnalyzer.isNumerical(value4);
        System.out.println(num);
        System.out.println(num2);
        System.out.println(num3);
        System.out.println(num4);

        value = value.replace(",", "");
        float f = Float.valueOf(value).floatValue();
        value2 = value2.replace(",", "");
        float f2 = Float.valueOf(value2).floatValue();
        value3 = value3.replace(",", "");
        float f3 = Float.valueOf(value3).floatValue();
        value4 = value4.replace(",", "");
        float f4 = Float.valueOf(value4).floatValue();

        // Other tests:

        String v = "6005262010";
        boolean integer = PreAnalyzer.isNumerical(v);
        System.out.println(integer);
        System.out.println(Integer.MAX_VALUE);
        long vint = Long.valueOf(v).longValue();

        String v2 = "999999999999999999999999999";
        boolean isNumber = PreAnalyzer.isNumerical(v);
        System.out.println(isNumber);
        System.out.println(Long.MAX_VALUE);
        // long parseLongNines = Long.valueOf(v2).longValue();
    }
}
