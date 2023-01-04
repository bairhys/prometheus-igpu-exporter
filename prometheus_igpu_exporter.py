from prometheus_client import start_http_server, Gauge
import sys
import subprocess
import json
import logging

igpu_engines_blitter_0_busy = Gauge('igpu_engines_blitter_0_busy', 'Blitter 0 busy utilisation %')
igpu_engines_blitter_0_sema = Gauge('igpu_engines_blitter_0_sema', 'Blitter 0 sema utilisation %')
igpu_engines_blitter_0_wait = Gauge('igpu_engines_blitter_0_wait', 'Blitter 0 wait utilisation %')

igpu_engines_render_3d_0_busy = Gauge('igpu_engines_render_3d_0_busy', 'Render 3D 0 busy utilisation %')
igpu_engines_render_3d_0_sema = Gauge('igpu_engines_render_3d_0_sema', 'Render 3D 0 sema utilisation %')
igpu_engines_render_3d_0_wait = Gauge('igpu_engines_render_3d_0_wait', 'Render 3D 0 wait utilisation %')

igpu_engines_video_0_busy = Gauge('igpu_engines_video_0_busy', 'Video 0 busy utilisation %')
igpu_engines_video_0_sema = Gauge('igpu_engines_video_0_sema', 'Video 0 sema utilisation %')
igpu_engines_video_0_wait = Gauge('igpu_engines_video_0_wait', 'Video 0 wait utilisation %')

igpu_engines_video_enhance_0_busy = Gauge('igpu_engines_video_enhance_0_busy', 'Video Enhance 0 busy utilisation %')
igpu_engines_video_enhance_0_sema = Gauge('igpu_engines_video_enhance_0_sema', 'Video Enhance 0 sema utilisation %')
igpu_engines_video_enhance_0_wait = Gauge('igpu_engines_video_enhance_0_wait', 'Video Enhance 0 wait utilisation %')

igpu_frequency_actual = Gauge('igpu_frequency_actual', 'Frequency actual MHz')
igpu_frequency_requested = Gauge('igpu_frequency_requested', 'Frequency requested MHz')

igpu_imc_bandwidth_reads = Gauge('igpu_imc_bandwidth_reads', 'IMC reads MiB/s')
igpu_imc_bandwidth_writes = Gauge('igpu_imc_bandwidth_writes', 'IMC writes MiB/s')

igpu_interrupts = Gauge('igpu_interrupts', 'Interrupts/s')

igpu_period = Gauge('igpu_period', 'Period ms')

igpu_power_gpu = Gauge('igpu_power_gpu', 'GPU power W')
igpu_power_package = Gauge('igpu_power_package', 'Package power W')

igpu_rc6 = Gauge('igpu_rc6', 'RC6 %')

def update(data):
    igpu_engines_blitter_0_busy.set(data['engines']['Blitter/0']['busy'])
    igpu_engines_blitter_0_sema.set(data['engines']['Blitter/0']['sema'])
    igpu_engines_blitter_0_wait.set(data['engines']['Blitter/0']['wait'])

    igpu_engines_render_3d_0_busy.set(data['engines']['Render/3D/0']['busy'])
    igpu_engines_render_3d_0_sema.set(data['engines']['Render/3D/0']['sema'])
    igpu_engines_render_3d_0_wait.set(data['engines']['Render/3D/0']['wait'])

    igpu_engines_video_0_busy.set(data['engines']['Video/0']['busy'])
    igpu_engines_video_0_sema.set(data['engines']['Video/0']['sema'])
    igpu_engines_video_0_wait.set(data['engines']['Video/0']['wait'])

    igpu_engines_video_enhance_0_busy.set(data['engines']['VideoEnhance/0']['busy'])
    igpu_engines_video_enhance_0_sema.set(data['engines']['VideoEnhance/0']['sema'])
    igpu_engines_video_enhance_0_wait.set(data['engines']['VideoEnhance/0']['wait'])

    igpu_frequency_actual.set(data['frequency']['actual'])
    igpu_frequency_requested.set(data['frequency']['requested'])

    igpu_imc_bandwidth_reads.set(data['imc-bandwidth']['reads'])
    igpu_imc_bandwidth_writes.set(data['imc-bandwidth']['writes'])

    igpu_interrupts.set(data['interrupts']['count'])

    igpu_period.set(data['period']['duration'])

    igpu_power_gpu.set(data['power']['GPU'])
    igpu_power_package.set(data['power']['Package'])

    igpu_rc6.set(data['rc6']['value'])

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    start_http_server(9100)
    
    period = 5000 #ms
    if len(sys.argv) > 1:
        period = sys.argv[1]

    cmd = '/usr/bin/intel_gpu_top -J -s {}'.format(int(period))
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    logging.info('Started ' + cmd)
    output = ''

    while process.poll() is None:
        read = process.stdout.readline()
        output+=read.decode('utf-8')
        if read == b'},\n':
            update(json.loads(output[:-2]))
            output = ''
    
    process.kill()

    if process.returncode != 0:
        logging.error("Error: " + process.stderr.read().decode('utf-8'))
    
    logging.info("Finished")